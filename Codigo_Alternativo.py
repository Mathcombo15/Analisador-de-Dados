# import pandas as pd
# import matplotlib.pyplot as plt
# from statistics import mode
# import os


# def carregar_dados():
#     """Carrega o arquivo CSV ou JSON fornecido pelo usuário."""
#     while True:
#         caminho = input("Digite o caminho completo do arquivo (CSV ou JSON): ").strip()
#         if not os.path.exists(caminho):
#             print("Arquivo não encontrado. Tente novamente.")
#             continue

#         try:
#             if caminho.lower().endswith('.csv'):
#                 dados = pd.read_csv(caminho)
#             elif caminho.lower().endswith('.json'):
#                 dados = pd.read_json(caminho)
#             else:
#                 print("Formato não suportado. Use CSV ou JSON.")
#                 continue
#             return dados
#         except Exception as e:
#             print(f"Erro ao carregar arquivo: {e}")


# def mostrar_resumo(dados):
#     """Exibe um resumo estatístico dos dados."""
#     print("\n=== RESUMO ESTATÍSTICO ===")
#     print(f"Total de registros: {len(dados)}")
#     print(f"Quantidade de homens: {len(dados[dados['Gender'] == 'Male'])}")
#     print(f"Quantidade de mulheres: {len(dados[dados['Gender'] == 'Female'])}")
#     print("Registros sem dados sobre educação dos pais: "
#           f"{dados['Parental_education'].isnull().sum()}")


# def limpar_dados(dados):
#     """Realiza a limpeza dos dados conforme especificado."""
#     # Remover registros com educação dos pais vazia
#     dados_limpos = dados.dropna(subset=['Parental_education'])
    
#     # Preencher Attendance nulo com a mediana
#     mediana_attendance = dados_limpos['Attendance'].median()
#     dados_limpos['Attendance'] = dados_limpos['Attendance'].fillna(mediana_attendance)
    
#     print(f"\nSomatório de Attendance: {dados_limpos['Attendance'].sum():.2f}")
#     return dados_limpos


# def consultar_coluna(dados):
#     """Permite ao usuário consultar estatísticas de uma coluna."""
#     colunas_disponiveis = [col for col in dados.columns if dados[col].dtype in ['int64', 'float64']]
#     print("\nColunas disponíveis para análise:")
#     for i, col in enumerate(colunas_disponiveis, 1):
#         print(f"{i}. {col}")

#     while True:
#         try:
#             escolha = int(input("\nDigite o número da coluna desejada: ")) - 1
#             if 0 <= escolha < len(colunas_disponiveis):
#                 coluna = colunas_disponiveis[escolha]
#                 break
#             print("Número inválido. Tente novamente.")
#         except ValueError:
#             print("Entrada inválida. Digite um número.")

#     print(f"\nEstatísticas para {coluna}:")
#     print(f"Média: {dados[coluna].mean():.2f}")
#     print(f"Mediana: {dados[coluna].median():.2f}")
#     try:
#         print(f"Moda: {mode(dados[coluna])}")
#     except:
#         print("Moda: múltiplos valores")
#     print(f"Desvio padrão: {dados[coluna].std():.2f}")


# def gerar_graficos(dados):
#     """Gera os gráficos especificados."""
#     plt.figure(figsize=(15, 10))
    
#     # Gráfico de dispersão: horas de sono x nota final
#     plt.subplot(2, 2, 1)
#     plt.scatter(dados['Sleep_time'], dados['Final_grade'], alpha=0.5)
#     plt.title('Horas de Sono vs Nota Final')
#     plt.xlabel('Horas de Sono')
#     plt.ylabel('Nota Final')
    
#     # Gráfico de barras: idade x média das notas intermediárias
#     plt.subplot(2, 2, 2)
#     idade_media = dados.groupby('Age')['Midterm_Score'].mean()
#     idade_media.plot(kind='bar')
#     plt.title('Idade vs Média das Notas Intermediárias')
#     plt.xlabel('Idade')
#     plt.ylabel('Média das Notas')
    
#     # Gráfico de pizza: faixas etárias
#     plt.subplot(2, 2, 3)
#     faixas = ['≤17', '18-21', '22-24', '25+']
#     cortes = [0, 17, 21, 24, 100]
#     dados['Faixa_etaria'] = pd.cut(dados['Age'], bins=cortes, labels=faixas)
#     contagem = dados['Faixa_etaria'].value_counts()
#     contagem.plot(kind='pie', autopct='%1.1f%%')
#     plt.title('Distribuição por Faixa Etária')
#     plt.ylabel('')
    
#     plt.tight_layout()
#     plt.show()


# def main():
#     """Função principal que orquestra o programa."""
#     print("=== ANALISADOR DE DADOS DE ESTUDANTES ===")
    
#     # Carregar dados
#     dados = carregar_dados()
    
#     # Mostrar resumo
#     mostrar_resumo(dados)
    
#     # Limpar dados
#     dados = limpar_dados(dados)
    
#     # Menu interativo
#     while True:
#         print("\n=== MENU ===")
#         print("1. Consultar estatísticas de uma coluna")
#         print("2. Visualizar gráficos")
#         print("3. Sair")
        
#         opcao = input("Escolha uma opção: ")
        
#         if opcao == '1':
#             consultar_coluna(dados)
#         elif opcao == '2':
#             gerar_graficos(dados)
#         elif opcao == '3':
#             print("Encerrando o programa...")
#             break
#         else:
#             print("Opção inválida. Tente novamente.")


# if __name__ == "__main__":
#     main()
import pandas as pd
import matplotlib.pyplot as plt



print("\n---- ANALISADOR DE DADOS ----")
print("\n*** [Carregando arquivo] ***")
# Primeiro Processo Geral: Carregar um arquivo CSV

# Carregar arquivo através do caminho do mesmo
caminhoArquivo = input("Escreva o caminho do arquivo para leitura: \n")
arquivo = pd.read_csv(caminhoArquivo)
num_dados = len(arquivo)

# Filtrar coluna 'Gender' e contar número de pessoas de cada genêro.
filtroMasculino = arquivo[arquivo["Gender"]=="Male"]
filtroFeminino = arquivo[arquivo["Gender"]=="Female"]
quantidadeHomens = len(filtroMasculino)
quantidadeMulheres = len(filtroFeminino)

filtroPais = arquivo[arquivo["Parent_Education_Level"].isna()]
educacao_pais_vazio = len(filtroPais)

print("\nRESUMO ESTATÍSCO DOS DADOS: ")
print(f"Registros carregados: {num_dados}.")
print(f"Quantidade de homens: {quantidadeHomens}.")
print(f"Quantidade de mulheres: {quantidadeMulheres}.")
print(f"Quantidade de registros com o campo 'Nível de educação dos pais' vazio: {educacao_pais_vazio}.\n")

print("\n*** [Limpeza de Dados] ***")
# arquivo2 = arquivo.dropna(subset=["Parent_Education_Level"])
print("\n*** [Consulta a Dados] ***")

print("\n*** [Gráficos] ***")

# arquivoNumerico = arquivo.select_dtypes(include=["number"])
# listaColunas = arquivoNumerico.columns.tolist()
# for i, coluna in enumerate(listaColunas): 
#     numeroColuna = i+1
#     print(f"{numeroColuna} - {coluna}")
# colunaEscolhida = input("\nEscolha a coluna que deseja calcular (escreva o número): ")
# colunaCalculo = listaColunas[int(colunaEscolhida) -1]

# valoresACalcular = arquivoNumerico[colunaCalculo].tolist()
# serie = pd.Series(valoresACalcular)
# media = serie.mean()
# mediana = serie.median()
# moda = serie.mode().iloc[0]
# desvioPadrao = serie.std()
# print(f"Média: {media}")
# print(f"Mediana: {mediana}")
# print(f"Moda: {moda}")
# print(f"Desvio padrão: {desvioPadrao}")

# plt.scatter(arquivoNumerico["Sleep_Hours_per_Night"], arquivoNumerico["Final_Score"])
# plt.title("Gráfico de Dispersão - Horas de sono x Nota final")
# plt.xlabel("Horas de Sono")
# plt.ylabel("Nota Final")
# plt.show()

# plt.bar(arquivoNumerico["Age"], arquivoNumerico["Midterm_Score"])
# plt.title("Gráfico de Barras - Idade x Média das Notas Intermediárias")
# plt.xlabel("Idade")
# plt.ylabel("Idade x Média das Notas Intermediárias")
# plt.show()

# filtro1 = arquivoNumerico[arquivoNumerico["Age"]<=17]
# faixaEtaria1 = len(filtro1)

# filtro2 = arquivoNumerico[(arquivoNumerico["Age"]> 17) &(arquivo["Age"]<=21)]
# faixaEtaria2 = len(filtro2)

# filtro3 = arquivoNumerico[(arquivoNumerico["Age"]> 21) &(arquivo["Age"]<=24)]
# faixaEtaria3 = len(filtro3)

# filtro4 = arquivoNumerico[arquivoNumerico["Age"]>24]
# faixaEtaria4 = len(filtro4)

# plt.pie([faixaEtaria1, faixaEtaria2, faixaEtaria3, faixaEtaria4], labels=["<17","18-21","22-24","25+"],autopct="%1.1f%%",startangle=90)
# plt.title("Gráfico de Pizza - Idades")
# plt.axis("equal")
# plt.show()