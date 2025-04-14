import pandas as pd
import matplotlib.pyplot as plt

def validar_arquivo_csv():
    """Valida e carrega um arquivo CSV com tratamento robusto de erros."""
    while True:
        caminho_arquivo = input("Escreva qual é o caminho do arquivo: ").strip()
        
        if not caminho_arquivo:
            print("Erro: O caminho do arquivo não pode estar vazio.")
            continue
            
        try:
            arquivo = pd.read_csv(caminho_arquivo)
            
            if len(arquivo) == 0:
                print("Aviso: O arquivo está vazio.")
            else:
                print(f"O arquivo contém {len(arquivo)} registros.")
            
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
        
        filtro_pais = arquivo[arquivo["Parent_Education_Level"].isna()]
        educacao_pais = len(filtro_pais)
        
        arquivo_sem_nulos = arquivo.dropna(subset=["Parent_Education_Level"])
        
        # Exibição de resultados
        print("\nResumo dos Dados:")
        print(f"Total de registros: {len(arquivo)}")
        print(f"Quantidade de homens: {quantidade_homens}")
        print(f"Quantidade de mulheres: {quantidade_mulheres}")
        print(f"Registros sem informação sobre educação dos pais: {educacao_pais}")
        
        return True
        
    except Exception as e:
        print(f"\nErro na análise de dados: {str(e)}")
        return False

def calcular_estatisticas(arquivo):
    """Calcula estatísticas para colunas numéricas."""
    try:
        arquivo_numerico = arquivo.select_dtypes(include=["number"])
        
        if arquivo_numerico.empty:
            print("Nenhuma coluna numérica encontrada para análise.")
            return
            
        lista_colunas = arquivo_numerico.columns.tolist()
        
        print("\nColunas numéricas disponíveis:")
        for i, coluna in enumerate(lista_colunas, 1):
            print(f"{i} - {coluna}")
            
        while True:
            try:
                escolha = input("\nEscolha a coluna que deseja calcular (número) ou 'sair': ")
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
    """Gera gráficos de análise dos dados."""
    try:
        # Gráfico de dispersão
        plt.figure(figsize=(10, 5))
        plt.scatter(arquivo["Sleep_Hours_per_Night"], arquivo["Final_Score"], alpha=0.5)
        plt.title("Relação entre Horas de Sono e Nota Final")
        plt.xlabel("Horas de Sono por Noite")
        plt.ylabel("Nota Final")
        plt.grid(True)
        plt.show()
        
        # Gráfico de barras
        plt.figure(figsize=(10, 5))
        media_idade = arquivo.groupby("Age")["Midterm_Score"].mean()
        media_idade.plot(kind='bar')
        plt.title("Média das Notas Intermediárias por Idade")
        plt.xlabel("Idade")
        plt.ylabel("Média das Notas")
        plt.xticks(rotation=0)
        plt.grid(True)
        plt.show()
        
        # Gráfico de pizza (faixas etárias)
        filtro1 = arquivo[arquivo["Age"] <= 17]
        filtro2 = arquivo[(arquivo["Age"] > 17) & (arquivo["Age"] <= 21)]
        filtro3 = arquivo[(arquivo["Age"] > 21) & (arquivo["Age"] <= 24)]
        filtro4 = arquivo[arquivo["Age"] > 24]
        
        tamanhos = [len(filtro1), len(filtro2), len(filtro3), len(filtro4)]
        rotulos = ["Até 17 anos", "18-21 anos", "22-24 anos", "25+ anos"]
        
        plt.figure(figsize=(8, 8))
        plt.pie(tamanhos, labels=rotulos, autopct="%1.1f%%", startangle=90,
                explode=(0.1, 0, 0, 0), shadow=True)
        plt.title("Distribuição por Faixa Etária")
        plt.axis('equal')
        plt.show()
        
    except KeyError as e:
        print(f"Erro: Coluna {str(e)} não encontrada para geração de gráficos.")
    except Exception as e:
        print(f"Erro na geração de gráficos: {str(e)}")

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