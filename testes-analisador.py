import pandas as pd
import matplotlib.pyplot as plt

print("\n---- ANALISADOR DE DADOS ----")
print("\n*** [Carregando arquivo] ***")
""" Primeiro Processo Geral: Carregar um arquivo CSV """

# Carregar arquivo através do caminho do mesmo com tratamento de erro
while True:
    try:
        caminhoArquivo = input("Escreva o caminho do arquivo para leitura: \n")
        arquivo = pd.read_csv(caminhoArquivo)
        break
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado. Por favor, verifique o caminho e tente novamente.")
    except Exception as e:
        print(f"Erro inesperado ao carregar o arquivo: {e}. Por favor, tente novamente.")

num_dados = len(arquivo)

# Filtrar coluna 'Gender' e contar número de pessoas de cada genêro.
try:
    filtroMasculino = arquivo[arquivo["Gender"]=="Male"]
    filtroFeminino = arquivo[arquivo["Gender"]=="Female"]
    quantidadeHomens = len(filtroMasculino)
    quantidadeMulheres = len(filtroFeminino)
except KeyError:
    print("Aviso: Coluna 'Gender' não encontrada no arquivo. Pulando esta análise.")
    quantidadeHomens = 0
    quantidadeMulheres = 0

# Contar número de campos vazios da coluna 'Nível de educação dos pais(Parent_Education_Level)'
try:
    filtroPais = arquivo[arquivo["Parent_Education_Level"].isna()]
    educacao_pais_vazio = len(filtroPais)
except KeyError:
    print("Aviso: Coluna 'Parent_Education_Level' não encontrada no arquivo. Pulando esta análise.")
    educacao_pais_vazio = 0

# Resumo estatísco 
print("\nRESUMO ESTATÍSCO DOS DADOS: ")
print(f"- Registros carregados: {num_dados}.")
print(f"- Quantidade de homens: {quantidadeHomens}.")
print(f"- Quantidade de mulheres: {quantidadeMulheres}.")
print(f"- Quantidade de registros com o campo 'Nível de educação dos pais' vazio: {educacao_pais_vazio}.")

print("\n*** [Limpeza de Dados] ***")
""" Segundo processo geral: Limpeza de dados do arquivo carregado """

# Remoção dos registros que estão com o campo 'Nível de educação dos pais' vazio
try:
    novo_arquivo = arquivo.dropna(subset=['Parent_Education_Level']) 
    print("\nATENÇÃO: Registros com o campo 'Nível de educação dos pais' vazios, foram removidos!")
except KeyError:
    print("\nAviso: Coluna 'Parent_Education_Level' não encontrada. Pulando esta etapa de limpeza.")
    novo_arquivo = arquivo.copy()

# Alteração de dados da coluna 'Presença(Attendance)' que estão nulos para a mediana
try:
    # Ordenar de forma crescente os valores da coluna 'Attendance' 
    print("\n- Coluna Attendance ordenada de forma crescente:")
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

    # Somatório dos valores da coluna 'Attendance'
    soma_attendance = novo_arquivo['Attendance (%)'].sum()
    print(f"\nSomatório da coluna Attendance: {soma_attendance}")
except KeyError:
    print("\nAviso: Coluna 'Attendance (%)' não encontrada. Pulando esta etapa de limpeza.")

print("\n*** [Consulta a Dados] ***")
""" Terceiro processo geral: Limpeza de dados do arquivo carregado """

# Apresentação de colunas para realização de cálculo posterior
arquivoNumerico = arquivo.select_dtypes(include=["number"])
listaColunas = arquivoNumerico.columns.tolist()

if not listaColunas:
    print("\nAviso: Nenhuma coluna numérica encontrada no arquivo. Não é possível realizar cálculos estatísticos.")
else:
    for i, coluna in enumerate(listaColunas): 
        numeroColuna = i+1
        print(f"{numeroColuna} - {coluna}")
    
    while True:
        try:
            colunaEscolhida = input("\nEscolha a coluna que deseja calcular (escreva o número): ")
            indice = int(colunaEscolhida) - 1
            
            if indice < 0 or indice >= len(listaColunas):
                print(f"Erro: Por favor, digite um número entre 1 e {len(listaColunas)}")
                continue
                
            colunaCalculo = listaColunas[indice]
            
            # Cálculo da 'Média', 'Mediana', 'Moda', e 'Desvio Padrão' da coluna escolhida pelo usuário
            valoresACalcular = arquivoNumerico[colunaCalculo].tolist()
            serie = pd.Series(valoresACalcular)
            media = serie.mean()
            mediana = serie.median()
            moda = serie.mode().iloc[0]
            desvioPadrao = serie.std()
            
            print(f"\nRESULTADO ESTATÍSTICO DA COLUNA {colunaEscolhida}:")
            print(f"- Média: {media:.2f}")
            print(f"- Mediana: {mediana:.2f}")
            print(f"- Moda: {moda:.2f}")
            print(f"- Desvio padrão: {desvioPadrao:.2f}")
            break
            
        except ValueError:
            print("Erro: Por favor, digite um número válido.")
        except Exception as e:
            print(f"Erro inesperado: {e}. Por favor, tente novamente.")

print("\n*** [Gráficos] ***")
print("""
      SR. USUÁRIO, UM GRÁFICO ACABA DE SER GERADO EM UMA NOVA ABA NA BARRA DE TAREFAS DO SEU COMPUTADOR. 
      AO FECHAR O GRÁFICO ATUAL, VOCÊ TERÁ ACESSO AO PRÓXIMO GRÁFICO LOGO EM SEGUIDA. 
      NO TOTAL, SERÃO GERADOS 3 GRÁFICOS.
      """)
""" Quarto processo geral: Visualização de gráficos gerados a partir das colunas abaixo """

plt.rcParams['figure.autolayout'] = True  # Ajuste automático do layout
plt.rcParams['axes.grid'] = True  # Grade habilitada por padrão
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.4

try:
    # 1. Gráfico de Dispersão (Horas de Sono x Nota Final)
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        arquivoNumerico["Sleep_Hours_per_Night"], 
        arquivoNumerico["Final_Score"],
        c=arquivoNumerico["Age"],  # Cores baseadas na idade
        cmap='viridis',
        alpha=0.7,
        edgecolors='w',
        linewidth=0.5
    )

    # Elementos do gráfico
    plt.colorbar(scatter, label='Idade (anos)')
    plt.title("Relação entre Horas de Sono e Nota Final", pad=20)
    plt.xlabel("Horas de Sono por Noite")
    plt.ylabel("Nota Final (pontos)")
    plt.grid(True)
    plt.show()
except KeyError as e:
    print(f"\nAviso: Não foi possível gerar o gráfico de dispersão. Coluna não encontrada: {e}")

try:
    # 2. Gráfico de Barras (Idade x Média de Notas)
    # Agrupar dados primeiro
    dados_agrupados = arquivoNumerico.groupby('Age')['Midterm_Score'].mean().reset_index()

    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        dados_agrupados["Age"].astype(str),  # Idades como strings
        dados_agrupados["Midterm_Score"],
        color='#1f77b4',  # Azul padrão do matplotlib
        edgecolor='black',
        width=0.7
    )

    # Adicionar valores em cima das barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}',
                 ha='center', 
                 va='bottom',
                 fontsize=9)

    plt.title("Média das Notas Intermediárias por Idade", pad=20)
    plt.xlabel("Idade (anos)")
    plt.ylabel("Média das Notas")
    plt.xticks(rotation=45)  # Rotacionar labels se necessário
    plt.grid(axis='y')
    plt.show()
except KeyError as e:
    print(f"\nAviso: Não foi possível gerar o gráfico de barras. Coluna não encontrada: {e}")

try:
    plt.figure(figsize=(10, 8))

    # Definindo faixas etárias e contagens
    faixas = ["≤17 anos", "18-21 anos", "22-24 anos", "25+ anos"]
    valores = [
        len(arquivoNumerico[arquivoNumerico["Age"] <= 17]),
        len(arquivoNumerico[(arquivoNumerico["Age"] > 17) & (arquivoNumerico["Age"] <= 21)]),
        len(arquivoNumerico[(arquivoNumerico["Age"] > 21) & (arquivoNumerico["Age"] <= 24)]),
        len(arquivoNumerico[arquivoNumerico["Age"] > 24])
    ]

    # Configurações visuais melhoradas
    cores = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB']
    explode = (0.05, 0, 0, 0)  # Destaque para a primeira fatia

    # Criando o gráfico
    wedges, texts, autotexts = plt.pie(
        valores,
        labels=faixas,
        autopct=lambda p: f'{p:.1f}%\n({int(p*sum(valores)/100)})',
        startangle=140,
        colors=cores,
        explode=explode,
        shadow=True,
        textprops={'fontsize': 11, 'color': '#333333'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'linestyle': 'solid'}
    )

    # Melhorando a legenda
    plt.setp(autotexts, size=11, weight="bold", color='white')
    plt.setp(texts, size=11, weight="bold")

    # Adicionando título e ajustes finais
    plt.title("Distribuição dos Alunos por Faixa Etária\n", 
              fontsize=14, pad=20, weight='bold')
    plt.subplots_adjust(top=0.85)  # Ajuste de espaço para o título

    # Adicionando legenda opcional
    plt.legend(wedges, faixas,
              title="Faixas Etárias",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()
    plt.show()
except KeyError as e:
    print(f"\nAviso: Não foi possível gerar o gráfico de pizza. Coluna não encontrada: {e}")