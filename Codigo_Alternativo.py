import pandas as pd
import matplotlib.pyplot as plt



print("\n---- ANALISADOR DE DADOS ----")
print("\n*** [Carregando arquivo] ***")
""" Primeiro Processo Geral: Carregar um arquivo CSV """

# Carregar arquivo através do caminho do mesmo
caminhoArquivo = input("Escreva o caminho do arquivo para leitura: \n")
arquivo = pd.read_csv(caminhoArquivo)
num_dados = len(arquivo)

# Filtrar coluna 'Gender' e contar número de pessoas de cada genêro.
filtroMasculino = arquivo[arquivo["Gender"]=="Male"]
filtroFeminino = arquivo[arquivo["Gender"]=="Female"]
quantidadeHomens = len(filtroMasculino)
quantidadeMulheres = len(filtroFeminino)

# Contar número de campos vazios da coluna 'Nível de educação dos pais(Parent_Education_Level)'
filtroPais = arquivo[arquivo["Parent_Education_Level"].isna()]
educacao_pais_vazio = len(filtroPais)

# Resumo estatísco 
print("\nRESUMO ESTATÍSCO DOS DADOS: ")
print(f"- Registros carregados: {num_dados}.")
print(f"- Quantidade de homens: {quantidadeHomens}.")
print(f"- Quantidade de mulheres: {quantidadeMulheres}.")
print(f"- Quantidade de registros com o campo 'Nível de educação dos pais' vazio: {educacao_pais_vazio}.")

print("\n*** [Limpeza de Dados] ***")
""" Segundo processo geral: Limpeza de dados do arquivo carregado """

# Remoção dos registros que estão com o campo 'Nível de educação dos pais' vazio
novo_arquivo = arquivo.dropna(subset=['Parent_Education_Level']) 
print("\nATENÇÃO: Registros com o campo 'Nível de educação dos pais' vazios, foram removidos!")
# print(novo_arquivo['Parent_Education_Level']) 

# Alteração de dados da coluna 'Presença(Attendance)' que estão nulos para a mediana

# Ordenar de forma crescente os valores da coluna 'Attendance' 
# ATENÇÂO: no método '.sort_values' valores nulos são colocados ao fim do DataFrame
print("\nATENÇÂO: Coluna Attendance ordenada de forma crescente!")
novo_arquivo_ordenado = novo_arquivo.sort_values(['Attendance (%)'])
attendance = novo_arquivo_ordenado['Attendance (%)']
print(attendance)

# Mediana dos valores não nulos da coluna 'Attendance'
mediana_col_attendance = novo_arquivo['Attendance (%)'].median()
print(f"\n- Mediana da coluna Attendance: {mediana_col_attendance} %.")

# Alteração de dados de presença (Attendance) que estão nulos para a mediana
novo_arquivo['Attendance (%)'] = novo_arquivo['Attendance (%)'].fillna(mediana_col_attendance)
print("\n- Valores nulos preenchidos com a mediana:")
print(novo_arquivo['Attendance (%)'])

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