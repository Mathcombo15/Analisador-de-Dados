import pandas as pd
import matplotlib.pyplot as plt


def carregar_dados():
    """Carrega os dados do arquivo CSV e retorna um DataFrame."""
    print("\n---- ANALISADOR DE DADOS ----")
    print("\n*** [Carregando arquivo] ***")
    
    caminho_arquivo = input("Escreva o caminho do arquivo para leitura: \n")
    return pd.read_csv(caminho_arquivo)


def gerar_resumo_estatistico(arquivo):
    """Gera um resumo estatístico básico dos dados."""
    num_dados = len(arquivo)
    
    filtro_masculino = arquivo[arquivo["Gender"] == "Male"]
    filtro_feminino = arquivo[arquivo["Gender"] == "Female"]
    quantidade_homens = len(filtro_masculino)
    quantidade_mulheres = len(filtro_feminino)
    
    filtro_pais = arquivo[arquivo["Parent_Education_Level"].isna()]
    educacao_pais_vazio = len(filtro_pais)

    print("\nRESUMO ESTATÍSTICO DOS DADOS: ")
    print(f"- Registros carregados: {num_dados}.")
    print(f"- Quantidade de homens: {quantidade_homens}.")
    print(f"- Quantidade de mulheres: {quantidade_mulheres}.")
    print(
        "- Quantidade de registros com o campo 'Nível de educação dos pais' "
        f"vazio: {educacao_pais_vazio}."
    )


def limpar_dados(arquivo):
    """Realiza a limpeza dos dados e retorna o DataFrame processado."""
    print("\n*** [Limpeza de Dados] ***")
    
    # Remoção de registros com educação dos pais vazia
    novo_arquivo = arquivo.dropna(subset=["Parent_Education_Level"])
    print(
        "\nATENÇÃO: Registros com o campo 'Nível de educação dos pais' "
        "vazios, foram removidos!"
    )

    # Preenchimento de valores nulos na coluna Attendance com a mediana
    print("\n- Coluna Attendance ordenada de forma crescente:")
    novo_arquivo_ordenado = novo_arquivo.sort_values(["Attendance (%)"])
    print(novo_arquivo_ordenado["Attendance (%)"])

    mediana_col_attendance = novo_arquivo["Attendance (%)"].median()
    print(f"\n- Mediana da coluna Attendance: {mediana_col_attendance} %.")

    novo_arquivo["Attendance (%)"] = novo_arquivo["Attendance (%)"].fillna(
        mediana_col_attendance
    )
    print("\n- Valores nulos preenchidos com a mediana:")
    print(novo_arquivo["Attendance (%)"])

    soma_attendance = novo_arquivo["Attendance (%)"].sum()
    print(f"\nSomatório da coluna Attendance: {soma_attendance}")

    return novo_arquivo


def consultar_dados(arquivo):
    """Permite ao usuário consultar estatísticas de uma coluna numérica."""
    print("\n*** [Consulta a Dados] ***")
    
    arquivo_numerico = arquivo.select_dtypes(include=["number"])
    lista_colunas = arquivo_numerico.columns.tolist()
    
    print("\nColunas numéricas disponíveis:")
    for i, coluna in enumerate(lista_colunas):
        print(f"{i + 1} - {coluna}")
    
    coluna_escolhida = input("\nEscolha a coluna que deseja calcular (escreva o número): ")
    coluna_calculo = lista_colunas[int(coluna_escolhida) - 1]

    serie = arquivo_numerico[coluna_calculo]
    print(f"\nEstatísticas para a coluna '{coluna_calculo}':")
    print(f"- Média: {serie.mean()}")
    print(f"- Mediana: {serie.median()}")
    print(f"- Moda: {serie.mode().iloc[0]}")
    print(f"- Desvio padrão: {serie.std()}")


def gerar_graficos(arquivo):
    """Gera os gráficos de análise dos dados"""
    print("\n*** [Gráficos] ***")
    arquivo_numerico = arquivo.select_dtypes(include=["number"])
    
    _gerar_grafico_dispersao(arquivo_numerico)
    _gerar_grafico_barras(arquivo_numerico)
    _gerar_grafico_pizza(arquivo_numerico)


def _gerar_grafico_dispersao(arquivo_numerico):
    """Gera gráfico de dispersão para horas de sono x nota final."""
    plt.scatter(
        arquivo_numerico["Sleep_Hours_per_Night"],
        arquivo_numerico["Final_Score"]
    )
    plt.title("Gráfico de Dispersão - Horas de sono x Nota final")
    plt.xlabel("Horas de Sono")
    plt.ylabel("Nota Final")
    plt.show()


def _gerar_grafico_barras(arquivo_numerico):
    """Gera gráfico de barras para idade x média das notas intermediárias."""
    plt.bar(
        arquivo_numerico["Age"],
        arquivo_numerico["Midterm_Score"]
    )
    plt.title("Gráfico de Barras - Idade x Média das Notas Intermediárias")
    plt.xlabel("Idade")
    plt.ylabel("Notas Intermediárias")
    plt.show()


def _gerar_grafico_pizza(arquivo_numerico):
    """Gera gráfico de pizza para distribuição de idades."""
    faixas_etarias = [
        (arquivo_numerico["Age"] <= 17, "<17"),
        ((arquivo_numerico["Age"] > 17) & (arquivo_numerico["Age"] <= 21), "18-21"),
        ((arquivo_numerico["Age"] > 21) & (arquivo_numerico["Age"] <= 24), "22-24"),
        (arquivo_numerico["Age"] > 24, "25+")
    ]
    
    valores = [len(arquivo_numerico[filtro]) for filtro, _ in faixas_etarias]
    labels = [label for _, label in faixas_etarias]
    
    plt.pie(
        valores,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Distribuição por Faixa Etária")
    plt.axis("equal")
    plt.show()


def main():
    """Função principal que orquestra a execução do programa."""
    dados = carregar_dados()
    gerar_resumo_estatistico(dados)
    dados_limpos = limpar_dados(dados)
    consultar_dados(dados_limpos)
    gerar_graficos(dados_limpos)


if __name__ == "__main__":
    main()