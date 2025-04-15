import pandas as pd
import matplotlib.pyplot as plt


def carregar_dados():
    """Carrega e analisa os dados iniciais do arquivo CSV com tratamento de erros."""
    print("\n---- ANALISADOR DE DADOS ----")
    print("\n*** [Carregando arquivo] ***")
    
    while True:
        caminho_arquivo = input("Escreva o caminho de um arquivo CSV para leitura: \n").strip()
        
        # Validações iniciais
        if not caminho_arquivo:
            print("Erro: O caminho do arquivo não pode estar vazio.\n")
            continue
            
        if not caminho_arquivo.lower().endswith('.csv'):
            print("Erro: O arquivo deve ter extensão .csv\n")
            continue
            
        try:
            # Tentativa de carregar o arquivo
            arquivo = pd.read_csv(caminho_arquivo)
            
            # Verifica se o arquivo não está vazio
            if len(arquivo) == 0:
                print("Erro: O arquivo CSV está vazio.\n")
                continue
                
            # Verifica se as colunas necessárias existem
            colunas_necessarias = ['Gender', 'Parent_Education_Level']
            colunas_faltantes = [col for col in colunas_necessarias if col not in arquivo.columns]
            
            if colunas_faltantes:
                print(f"Erro: O arquivo não contém as colunas obrigatórias: {', '.join(colunas_faltantes)}\n")
                continue
            
            # Análise inicial
            num_dados = len(arquivo)
            filtro_masculino = arquivo[arquivo["Gender"] == "Male"]
            filtro_feminino = arquivo[arquivo["Gender"] == "Female"]
            educacao_pais_vazio = len(arquivo[arquivo["Parent_Education_Level"].isna()])
            
            print("\nRESUMO ESTATÍSTICO DOS DADOS: ")
            print(f"- Registros carregados: {num_dados}.")
            print(f"- Quantidade de homens: {len(filtro_masculino)}.")
            print(f"- Quantidade de mulheres: {len(filtro_feminino)}.")
            print(f"- Registros com campo 'Nível de educação dos pais' vazios: {educacao_pais_vazio}.")
            
            return arquivo
            
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado no caminho: {caminho_arquivo}\n")
        except pd.errors.EmptyDataError:
            print("Erro: O arquivo está vazio.\n")
        except pd.errors.ParserError:
            print("Erro: O arquivo não está no formato CSV válido.\n")
        except UnicodeDecodeError:
            print("Erro: Problema de codificação no arquivo. Use UTF-8.\n")
        except Exception as e:
            print(f"Erro inesperado: {str(e)}\n")
            
def limpar_dados(arquivo):
    """Realiza a limpeza e tratamento dos dados com tratamento robusto de erros."""
    print("\n*** [Limpeza de Dados] ***")
    
    # Cria uma cópia do arquivo original para não modificar o input
    novo_arquivo = arquivo.copy()
    
    # Remoção dos registros com educação dos pais vazia
    try:
        antes = len(novo_arquivo)
        novo_arquivo.dropna(subset=['Parent_Education_Level'], inplace=True)
        removidos = antes - len(novo_arquivo)
        print(f"\nATENÇÃO: Registros com campo 'Nível de educação dos pais' vazios foram removidos!")
    except KeyError:
        print("\nAVISO: Coluna 'Parent_Education_Level' não encontrada. Pulando esta etapa de limpeza.")
    
    # Tratamento da coluna Attendance
    try:
        # 1º Passo: Ordenação e visualização dos dados
        print("\n- Coluna Attendance ordenada de forma crescente:")
        novo_arquivo_ordenado = novo_arquivo.sort_values(['Attendance (%)'])
        print(novo_arquivo_ordenado['Attendance (%)'])
        
        # 2º Passo: Cálculo e aplicação da mediana
        mediana = novo_arquivo['Attendance (%)'].median()
        novo_arquivo['Attendance (%)'].fillna(mediana, inplace=True)
        
        # 3º Passo: Exibição estatística
        print(f"\n- Mediana da coluna Attendance: {mediana} %.")
        print("\n- Valores nulos preenchidos com a mediana:")
        print(novo_arquivo['Attendance (%)'])
        print(f"\n- Somatório da coluna Attendance: {novo_arquivo['Attendance (%)'].sum()}")
        
    except KeyError:
        print("\nAVISO: Coluna 'Attendance (%)' não encontrada. Pulando esta etapa de limpeza.")
    except Exception as e:
        print(f"\nERRO inesperado ao processar coluna Attendance: {str(e)}")
    
    return novo_arquivo

def consultar_dados(arquivo):
    """Permite ao usuário consultar estatísticas das colunas numéricas."""
    print("\n*** [Consulta a Dados] ***")
    print("""
          SR. USUÁRIO, ABAIXO ESTÃO AS COLUNAS DO ARQUIVO CSV FORNECIDO, PASSÍVEIS
          DE CÁLCULOS NÚMERICOS COMO: MÉDIA, MEDIANA, MODA E DESVIO PADRÃO.\n
          """)
    
    arquivo_numerico = arquivo.select_dtypes(include=["number"])
    lista_colunas = arquivo_numerico.columns.tolist()
    
    for i, coluna in enumerate(lista_colunas):
        print(f"{i+1} - {coluna}")
    
    coluna_escolhida = input("\nEscolha a coluna que deseja calcular (escreva um número): ")
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
    NA BARRA DE TAREFAS DO SEU COMPUTADOR. AO FECHAR O GRÁFICO ATUAL, 
    VOCÊ TERÁ ACESSO AO PRÓXIMO. NO TOTAL, SERÃO GERADOS 3 GRÁFICOS.
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
    plt.title("Relação entre Horas de Sono e Nota Final", pad=20)
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
        edgecolor='black',
        width=0.7
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{height:.1f}', ha='center', va='bottom')
    plt.title("Média das Notas Intermediárias por Idade", pad=20)
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
    
    plt.figure(figsize=(12, 6))
    plt.pie(
        valores,
        labels=faixas,
        autopct=lambda p: f'{p:.1f}%\n({int(p*sum(valores)/100)})',
        colors=['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB'],
        startangle=140,
        pctdistance=0.85,
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'}
    )
    
    
    plt.title("Distribuição dos Alunos por Faixa Etária", pad=20)
    plt.tight_layout()
    plt.show() 


def main():
    """Função principal que orquestra a execução do programa."""
    dados_brutos = carregar_dados()
    dados_limpos = limpar_dados(dados_brutos)
    dados_numericos = consultar_dados(dados_limpos)
    gerar_graficos(dados_numericos)

if __name__ == "__main__":
    main()