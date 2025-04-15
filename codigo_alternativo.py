import pandas as pd
import matplotlib.pyplot as plt


def carregar_dados():
    """Carrega e analisa os dados iniciais do arquivo CSV."""
    print("\n---- ANALISADOR DE DADOS ----")
    print("\n*** [Carregando arquivo] ***")
    
    caminho_arquivo = input("Escreva o caminho do arquivo para leitura: \n")
    arquivo = pd.read_csv(caminho_arquivo)
    
    # Análise inicial
    num_dados = len(arquivo)
    filtro_masculino = arquivo[arquivo["Gender"] == "Male"]
    filtro_feminino = arquivo[arquivo["Gender"] == "Female"]
    educacao_pais_vazio = len(arquivo[arquivo["Parent_Education_Level"].isna()])
    
    print("\nRESUMO ESTATÍSTICO DOS DADOS: ")
    print(f"- Registros carregados: {num_dados}.")
    print(f"- Quantidade de homens: {len(filtro_masculino)}.")
    print(f"- Quantidade de mulheres: {len(filtro_feminino)}.")
    print(f"- Campos 'Nível de educação dos pais' vazios: {educacao_pais_vazio}.")
    
    return arquivo


def limpar_dados(arquivo):
    """Realiza a limpeza e tratamento dos dados."""
    print("\n*** [Limpeza de Dados] ***")
    
    # Remover registros com educação dos pais vazia
    novo_arquivo = arquivo.dropna(subset=['Parent_Education_Level'])
    print("\nATENÇÃO: Registros com campo 'Nível de educação dos pais' vazios foram removidos!")
    
    # Tratar valores nulos na coluna Attendance
    mediana = novo_arquivo['Attendance (%)'].median()
    novo_arquivo['Attendance (%)'] = novo_arquivo['Attendance (%)'].fillna(mediana)
    
    print(f"\n- Mediana da coluna Attendance: {mediana} %.")
    print("\n- Valores nulos preenchidos com a mediana:")
    print(novo_arquivo['Attendance (%)'])
    print(f"\nSomatório da coluna Attendance: {novo_arquivo['Attendance (%)'].sum()}")
    
    return novo_arquivo


def consultar_dados(arquivo):
    """Permite ao usuário consultar estatísticas das colunas numéricas."""
    print("\n*** [Consulta a Dados] ***")
    
    arquivo_numerico = arquivo.select_dtypes(include=["number"])
    lista_colunas = arquivo_numerico.columns.tolist()
    
    for i, coluna in enumerate(lista_colunas):
        print(f"{i+1} - {coluna}")
    
    coluna_escolhida = input("\nEscolha a coluna que deseja calcular (escreva o número): ")
    coluna_calculo = lista_colunas[int(coluna_escolhida)-1]
    
    serie = pd.Series(arquivo_numerico[coluna_calculo].tolist())
    print(f"\n- Média: {serie.mean()}")
    print(f"- Mediana: {serie.median()}")
    print(f"- Moda: {serie.mode().iloc[0]}")
    print(f"- Desvio padrão: {serie.std()}")
    
    return arquivo_numerico


def gerar_graficos(arquivo_numerico):
    """Gera os gráficos de análise dos dados."""
    print("\n*** [Gráficos] ***")
    print("""
    SR. USUÁRIO, UM GRÁFICO ACABA DE SER GERADO EM UMA NOVA ABA. 
    AO FECHAR O GRÁFICO ATUAL, VOCÊ TERÁ ACESSO AO PRÓXIMO.
    NO TOTAL, SERÃO GERADOS 3 GRÁFICOS.
    """)
    
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.4

    # Gráfico 1: Dispersão (Horas de Sono x Nota Final)
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        arquivo_numerico["Sleep_Hours_per_Night"],
        arquivo_numerico["Final_Score"],
        c=arquivo_numerico["Age"],
        cmap='viridis',
        alpha=0.7
    )
    plt.colorbar(scatter, label='Idade (anos)')
    plt.title("Relação entre Horas de Sono e Nota Final")
    plt.xlabel("Horas de Sono por Noite")
    plt.ylabel("Nota Final (pontos)")
    plt.show()

    # Gráfico 2: Barras (Idade x Média de Notas)
    dados_agrupados = arquivo_numerico.groupby('Age')['Midterm_Score'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        dados_agrupados["Age"].astype(str),
        dados_agrupados["Midterm_Score"],
        color='#1f77b4',
        edgecolor='black'
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{height:.1f}', ha='center', va='bottom')
    plt.title("Média das Notas Intermediárias por Idade")
    plt.xlabel("Idade (anos)")
    plt.ylabel("Média das Notas")
    plt.xticks(rotation=45)
    plt.show()

    # Gráfico 3: Pizza (Distribuição por Faixa Etária)
    faixas = ["≤17 anos", "18-21 anos", "22-24 anos", "25+ anos"]
    valores = [
        len(arquivo_numerico[arquivo_numerico["Age"] <= 17]),
        len(arquivo_numerico[(arquivo_numerico["Age"] > 17) & (arquivo_numerico["Age"] <= 21)]),
        len(arquivo_numerico[(arquivo_numerico["Age"] > 21) & (arquivo_numerico["Age"] <= 24)]),
        len(arquivo_numerico[arquivo_numerico["Age"] > 24])
    ]
    plt.figure(figsize=(10, 8))
    plt.pie(
        valores,
        labels=faixas,
        autopct=lambda p: f'{p:.1f}%\n({int(p*sum(valores)/100)})',
        colors=['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB'],
        startangle=140
    )
    plt.title("Distribuição dos Alunos por Faixa Etária")
    plt.show()


def main():
    """Função principal que orquestra a execução do programa."""
    dados_brutos = carregar_dados()
    dados_limpos = limpar_dados(dados_brutos)
    dados_numericos = consultar_dados(dados_limpos)
    gerar_graficos(dados_numericos)


if __name__ == "__main__":
    main()