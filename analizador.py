import pandas as pd
import matplotlib.pyplot as plt

caminhoArquivo = input("Escreva qual é o caminho do arquivo: ")
arquivo = pd.read_csv(caminhoArquivo)
num_dados = len(arquivo)

filtroMasculino = arquivo[arquivo["Gender"]=="Male"]
filtroFeminino = arquivo[arquivo["Gender"]=="Female"]

quantidadeHomens = len(filtroMasculino)
quantidadeMulheres = len(filtroFeminino)


filtroPais = arquivo[arquivo["Parent_Education_Level"].isna()]
educacaoPais = len(filtroPais)

arquivo2 = arquivo.dropna(subset=["Parent_Education_Level"])

print("Resumo dos Dados: ")
print(f"A quantidade de dados carregados é {num_dados}.")
print(f" A quantidade de homens é {quantidadeHomens}.")
print(f" A quantidade de mulheres é {quantidadeMulheres}.")
print(f" A quantidade de registros sem informação sobre a educação dos pais é {educacaoPais}.")

arquivoNumerico = arquivo.select_dtypes(include=["number"])
listaColunas = arquivoNumerico.columns.tolist()
for i, coluna in enumerate(listaColunas): 
    numeroColuna = i+1
    print(f"{numeroColuna} - {coluna}")
colunaEscolhida = input("Escolha a coluna que deseja calcular (escreva o número): ")
colunaCalculo = listaColunas[int(colunaEscolhida) -1]

valoresACalcular = arquivoNumerico[colunaCalculo].tolist()
serie = pd.Series(valoresACalcular)
media = serie.mean()
mediana = serie.median()
moda = serie.mode().iloc[0]
desvioPadrao = serie.std()
print(f"média: {media}")
print(f"mediana: {mediana}")
print(f"moda: {moda}")
print(f"desvio padrão: {desvioPadrao}")

plt.scatter(arquivoNumerico["Sleep_Hours_per_Night"], arquivoNumerico["Final_Score"])
plt.title("Gráfico de Dispersão - Horas de sono x Nota final")
plt.xlabel("Horas de Sono")
plt.ylabel("Nota Final")
plt.show()

plt.bar(arquivoNumerico["Age"], arquivoNumerico["Midterm_Score"])
plt.title("Gráfico de Barras - Idade x Média das Notas Intermediárias")
plt.xlabel("Idade")
plt.ylabel("Idade x Média das Notas Intermediárias")
plt.show()

filtro1 = arquivoNumerico[arquivoNumerico["Age"]<=17]
faixaEtaria1 = len(filtro1)

filtro2 = arquivoNumerico[(arquivoNumerico["Age"]> 17) &(arquivo["Age"]<=21)]
faixaEtaria2 = len(filtro2)

filtro3 = arquivoNumerico[(arquivoNumerico["Age"]> 21) &(arquivo["Age"]<=24)]
faixaEtaria3 = len(filtro3)

filtro4 = arquivoNumerico[arquivoNumerico["Age"]>24]
faixaEtaria4 = len(filtro4)

plt.pie([faixaEtaria1, faixaEtaria2, faixaEtaria3, faixaEtaria4], labels=["<17","18-21","22-24","25+"],autopct="%1.1f%%",startangle=90)
plt.title("Gráfico de Pizza - Idades")
plt.axis("equal")
plt.show()