import pandas as pd
import matplotlib.pyplot as plt
import statistics
from pathlib import Path

def main():
    print("=== Sistema de Análise de Dados de Alunos ===")
    
    # Carregar dados
    file_path = input("Digite o caminho completo do arquivo (CSV ou JSON): ")
    data = load_data(file_path)
    
    if data is not None:
        # Exibir resumo estatístico
        show_summary(data)
        
        # Limpeza de dados
        cleaned_data = clean_data(data)
        
        # Consultas estatísticas
        column_stats(cleaned_data)
        
        # Gerar gráficos
        generate_plots(cleaned_data)

def load_data(file_path):
    """Carrega os dados do arquivo CSV ou JSON"""
    try:
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.csv':
            return pd.read_csv(file_path)
        elif file_extension == '.json':
            return pd.read_json(file_path)
        else:
            print("Formato de arquivo não suportado. Use CSV ou JSON.")
            return None
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None
    
def show_summary(data):
    """Exibe um resumo estatístico dos dados"""
    print("\n=== Resumo Estatístico ===")
    
    # Quantidade de dados carregados
    print(f"Total de registros: {len(data)}")
    
    # Quantidade de homens e mulheres
    if 'Gender' in data.columns:
        gender_counts = data['Gender'].value_counts()
        print(f"\nDistribuição por gênero:")
        print(f"Homens: {gender_counts.get('male', 0)}")
        print(f"Mulheres: {gender_counts.get('female', 0)}")
    
    # Quantos registros sem dados sobre a educação dos pais
    if 'ParentEduc' in data.columns:
        missing_educ = data['ParentEduc'].isnull().sum()
        print(f"\nRegistros sem dados sobre educação dos pais: {missing_educ}")
        
def clean_data(data):
    """Realiza a limpeza dos dados conforme especificado"""
    print("\n=== Limpeza de Dados ===")
    
    # Remover registros com educação dos pais vazios
    if 'ParentEduc' in data.columns:
        cleaned = data.dropna(subset=['ParentEduc'])
        removed = len(data) - len(cleaned)
        print(f"Removidos {removed} registros com educação dos pais vazia")
    else:
        cleaned = data.copy()
    
    # Alterar dados de presença (Attendance) null para a mediana
    if 'Attendance' in cleaned.columns:
        median_attendance = cleaned['Attendance'].median()
        null_count = cleaned['Attendance'].isnull().sum()
        cleaned['Attendance'].fillna(median_attendance, inplace=True)
        print(f"Substituídos {null_count} valores nulos em Attendance pela mediana ({median_attendance})")
    
    # Apresentar somatório de Attendance
    if 'Attendance' in cleaned.columns:
        print(f"Somatório de Attendance: {cleaned['Attendance'].sum():.2f}")
    
    return cleaned

def column_stats(data):
    """Permite ao usuário escolher uma coluna e ver estatísticas"""
    print("\n=== Consulta Estatística por Coluna ===")
    
    # Listar colunas numéricas disponíveis
    numeric_cols = data.select_dtypes(include=['number']).columns
    print("Colunas numéricas disponíveis:")
    for i, col in enumerate(numeric_cols, 1):
        print(f"{i}. {col}")
    
    # Obter escolha do usuário
    while True:
        try:
            choice = int(input("\nDigite o número da coluna para ver estatísticas (0 para sair): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(numeric_cols):
                col_name = numeric_cols[choice-1]
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
    
    # Calcular e mostrar estatísticas
# col_data = data[col_name]
    
# print(f"\nEstatísticas para '{col_name}':")
# print(f"Média: {col_data.mean():.2f}")
# print(f"Mediana: {col_data.median():.2f}")
    
# try:
#     mode = statistics.mode(col_data)
#     print(f"Moda: {mode:.2f}")
# except statistics.StatisticsError:
#     print("Moda: Não há uma moda única")
    
#     print(f"Desvio Padrão: {col_data.std():.2f}")

def generate_plots(data):
    """Gera os gráficos especificados"""
    print("\n=== Gerando Gráficos ===")
    
    # Gráfico de dispersão para "horas de sono" x "nota final"
    if 'SleepHours' in data.columns and 'FinalGrade' in data.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(data['SleepHours'], data['FinalGrade'], alpha=0.5)
        plt.title('Relação entre Horas de Sono e Nota Final')
        plt.xlabel('Horas de Sono')
        plt.ylabel('Nota Final')
        plt.grid(True)
        plt.show()
    
    # Gráfico de barras – idade x média das notas intermediárias
    if 'Age' in data.columns and 'MidtermScore' in data.columns:
        age_midterm = data.groupby('Age')['MidtermScore'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(age_midterm['Age'], age_midterm['MidtermScore'])
        plt.title('Média das Notas Intermediárias por Idade')
        plt.xlabel('Idade')
        plt.ylabel('Média das Notas Intermediárias')
        plt.xticks(age_midterm['Age'])
        plt.grid(True, axis='y')
        plt.show()
    
    # Gráfico de pizza para as idades (Agrupadas)
    if 'Age' in data.columns:
        # Criar grupos de idade
        bins = [0, 17, 21, 24, data['Age'].max()+1]
        labels = ['Até 17', '18 a 21', '22 a 24', '25 ou mais']
        age_groups = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
        
        # Contar ocorrências em cada grupo
        age_counts = age_groups.value_counts()
        
        # Gerar gráfico de pizza
        plt.figure(figsize=(8, 8))
        plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribuição dos Alunos por Faixa Etária')
        plt.show()

if __name__ == "__main__":
    main()

