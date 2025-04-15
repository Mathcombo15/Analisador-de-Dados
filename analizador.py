import pandas as pd
import matplotlib.pyplot as plt

def validar_arquivo_csv():
    """Carrega e analisa os dados iniciais do arquivo CSV com tratamento de erros."""
    print("\n---- ANALISADOR DE DADOS ----")
    print("\n*** [Carregando arquivo] ***")
    
    while True:
        caminho_arquivo = input("Escreva qual é o caminho do arquivo: \n").strip()
        
        if not caminho_arquivo:
            print("Erro: O caminho do arquivo não pode estar vazio.")
            continue
            
        try:
            arquivo = pd.read_csv(caminho_arquivo)        
            return arquivo
            
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado no caminho: {caminho_arquivo}")
        except pd.errors.EmptyDataError:
            print("Erro: O arquivo está vazio.")
        except pd.errors.ParserError:
            print("Erro: O arquivo não está no formato CSV válido.")
        except UnicodeDecodeError:
            print("Erro: Problema de codificação no arquivo. Tente um arquivo com codificação diferente.")
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")

def analisar_dados(arquivo):
    """Realiza análise dos dados com tratamento de erros."""
    try:
        # Verificação de colunas necessárias
        colunas_necessarias = ['Gender', 'Parent_Education_Level', 'Age', 
                              'Sleep_Hours_per_Night', 'Final_Score', 'Midterm_Score']
        
        for coluna in colunas_necessarias:
            if coluna not in arquivo.columns:
                raise KeyError(f"Coluna '{coluna}' não encontrada no arquivo.")

        # Filtros e cálculos básicos
        filtro_masculino = arquivo[arquivo["Gender"] == "Male"]
        filtro_feminino = arquivo[arquivo["Gender"] == "Female"]
        
        quantidade_homens = len(filtro_masculino)
        quantidade_mulheres = len(filtro_feminino)
        
        educacao_pais = 0  # Inicializa a variável
        try:
            filtro_pais = arquivo[arquivo["Parent_Education_Level"].isna()]
            educacao_pais = len(filtro_pais)
            arquivo_sem_nulos = arquivo.dropna(subset=["Parent_Education_Level"])
        except KeyError:
            print("\nAVISO: Coluna 'Parent_Education_Level' não encontrada. Pulando esta etapa de limpeza.")
    
        # Exibição de resultados
        print("\nRESUMO ESTATÍSTICO DOS DADOS: ")
        print(f"- Registros carregados: {len(arquivo)}")
        print(f"- Quantidade de homens: {quantidade_homens}")
        print(f"- Quantidade de mulheres: {quantidade_mulheres}")
        print(f"- Registros com campo 'Nível de educação dos pais' vazios: {educacao_pais}")
        
        return True
        
    except Exception as e:
        print(f"\nErro na análise de dados: {str(e)}")
        return False

def calcular_estatisticas(arquivo):
    """Permite ao usuário consultar estatísticas das colunas numéricas."""
    print("\n*** [Consulta a Dados] ***")
    print("""
          SR. USUÁRIO, ABAIXO ESTÃO AS COLUNAS DO ARQUIVO CSV FORNECIDO, PASSÍVEIS
          DE CÁLCULOS NÚMERICOS COMO: MÉDIA, MEDIANA, MODA E DESVIO PADRÃO.\n
          """)
    
    try:
        arquivo_numerico = arquivo.select_dtypes(include=["number"])
        
        if arquivo_numerico.empty:
            print("Nenhuma coluna numérica encontrada para análise.")
            return
            
        lista_colunas = arquivo_numerico.columns.tolist()
        
        print("\nEscolha a coluna que deseja calcular (escreva o número): ")
        for i, coluna in enumerate(lista_colunas, 1):
            print(f"{i} - {coluna}")
            
        while True:
            try:
                escolha = input("\nEscolha a coluna que deseja calcular (escreva o número): ")
                if escolha.lower() == 'sair':
                    break
                    
                indice = int(escolha) - 1
                coluna_calculo = lista_colunas[indice]
                
                serie = arquivo_numerico[coluna_calculo]
                print(f"\nEstatísticas para {coluna_calculo}:")
                print(f"Média: {serie.mean():.2f}")
                print(f"Mediana: {serie.median():.2f}")
                print(f"Moda: {serie.mode().iloc[0]:.2f}")
                print(f"Desvio padrão: {serie.std():.2f}")
                print(f"Valor mínimo: {serie.min():.2f}")
                print(f"Valor máximo: {serie.max():.2f}")
                
            except (ValueError, IndexError):
                print("Entrada inválida. Digite um número correspondente à coluna ou 'sair'.")
            except Exception as e:
                print(f"Erro ao calcular estatísticas: {str(e)}")

    except Exception as e:
        print(f"Erro na seleção de colunas numéricas: {str(e)}")

def gerar_graficos(arquivo):
    """Gera os gráficos de análise dos dados."""
    print("\n*** [Gráficos] ***")
    print("""
    SR. USUÁRIO, UM GRÁFICO ACABA DE SER GERADO EM UMA NOVA ABA. 
    NA BARRA DE TAREFAS DO SEU COMPUTADOR, AO FECHAR O GRÁFICO ATUAL, VOCÊ TERÁ ACESSO AO PRÓXIMO.
    NO TOTAL, SERÃO GERADOS 3 GRÁFICOS.
    """)

    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.4

    # Cria o DataFrame numérico para os gráficos
    arquivo_numerico = arquivo.select_dtypes(include=["number"])
    
    # Verifica se as colunas necessárias existem
    colunas_graficos = ['Sleep_Hours_per_Night', 'Final_Score', 'Age', 'Midterm_Score']
    for coluna in colunas_graficos:
        if coluna not in arquivo_numerico.columns:
            print(f"Erro: Coluna '{coluna}' não encontrada para gerar gráficos.")
            return

    # Gráfico de dispersão
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
        
    # Gráfico de barras
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
        
    # Gráfico de pizza (faixas etárias)
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
    print("=== Análise de Dados Educacionais ===")
    
    # Carrega o arquivo
    arquivo = validar_arquivo_csv()
    
    if arquivo is None:
        return
        
    # Realiza análise básica
    if not analisar_dados(arquivo):
        return
        
    # Menu de opções
    while True:
        print("\nOpções:")
        print("1 - Calcular estatísticas de colunas numéricas")
        print("2 - Gerar gráficos de análise")
        print("3 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            calcular_estatisticas(arquivo)
        elif opcao == "2":
            gerar_graficos(arquivo)
        elif opcao == "3":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()