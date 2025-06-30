from faker import Faker
from csv_para_array import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Um estilo de gráfico que se assemelha ao ggplot2 do R
plt.style.use('ggplot')
# Define uma paleta de cores para os gráficos do Seaborn
sns.set_palette('viridis')
# Define um tema com grade branca para os gráficos do Seaborn
sns.set_theme(style="whitegrid")

# Para gerar nomes e outros dados mais realistas

# Inicializa o gerador de dados falsos
fake = Faker('pt_BR')  # Usamos 'pt_BR' para dados mais brasileiros

# Definindo o número de assinantes que queremos gerar
num_assinantes = 1000

# Listas para armazenar os dados gerados
dados = {
    'ID_Assinante': [],
    'Nome': [],
    'Email': [],
    'Data_Registro': [],
    'Idade': [],
    'Localizacao': [],
    'Plano_Assinatura': [],  # Ex: 'Básico', 'Premium', 'Família'
    'Status_Assinatura': [],  # Ex: 'Ativo', 'Cancelado'
    'Meses_Ativo': [],
    'Receita_Mensal': []
}

# Definindo os planos de assinatura e seus preços
planos = {
    'Básico': 19.90,
    'Premium': 29.90,
    'Família': 49.90
}
lista_planos = list(planos.keys())

# Gerando os dados para cada assinante
for i in range(num_assinantes):
    dados['ID_Assinante'].append(i + 1)
    dados['Nome'].append(fake.name())
    dados['Email'].append(fake.email())

    # Data de registro: aleatória nos últimos 3 anos
    data_registro = fake.date_between(start_date='-3y', end_date='today')
    dados['Data_Registro'].append(data_registro)

    dados['Idade'].append(np.random.randint(
        18, 65))  # Idade entre 18 e 65 anos
    # Sigla do estado brasileiro
    dados['Localizacao'].append(fake.state_abbr())

    # Escolhendo um plano aleatoriamente, com maior probabilidade para o Premium
    # 30% Básico, 50% Premium, 20% Família
    plano_escolhido = np.random.choice(lista_planos, p=[0.3, 0.5, 0.2])
    dados['Plano_Assinatura'].append(plano_escolhido)

    # Status da assinatura: 85% ativo, 15% cancelado
    status = np.random.choice(['Ativo', 'Cancelado'], p=[0.85, 0.15])
    dados['Status_Assinatura'].append(status)

    # Meses ativo: Se cancelado, um número menor de meses; se ativo, pode ser mais
    if status == 'Cancelado':
        # Cancelou em até 18 meses
        dados['Meses_Ativo'].append(np.random.randint(1, 18))
    else:
        dados['Meses_Ativo'].append(
            np.random.randint(1, 36))  # Ativo por até 36 meses

    # Receita Mensal baseada no plano
    dados['Receita_Mensal'].append(planos[plano_escolhido])

# Criando o DataFrame do Pandas
df_assinantes = pd.DataFrame(dados)
df_assinantes['Data_Registro'] = pd.to_datetime(df_assinantes['Data_Registro'])

# Exibindo as primeiras linhas do DataFrame e algumas informações para verificar
print("Primeiras 5 linhas do DataFrame de Assinantes:")
print(df_assinantes.head())

print("\nInformações sobre o DataFrame:")
df_assinantes.info()

# Verificando novamente os tipos de dados
print("Tipos de dados antes dos ajustes:")
print(df_assinantes.info())

# Verificando valores ausentes
print("\nContagem de valores ausentes por coluna:")
print(df_assinantes.isnull().sum())

# Verificando Linhas Duplicadas
print("\nNúmero de linhas duplicadas antes da remoção:")
print(df_assinantes.duplicated().sum())

# 1. Extrair Mês e Ano da Data_Registro
df_assinantes['Mes_Registro'] = df_assinantes['Data_Registro'].dt.month
df_assinantes['Ano_Registro'] = df_assinantes['Data_Registro'].dt.year

# 2. Calcular Custo Total da Assinatura (para assinantes ativos e cancelados)
df_assinantes['Custo_Total_Assinatura'] = df_assinantes['Meses_Ativo'] * \
    df_assinantes['Receita_Mensal']

# 3. Criar Faixa Etária
bins = [18, 25, 35, 45, 55, 65]  # Limites de idade
labels = ['18-24', '25-34', '35-44', '45-54', '55-64']  # Nomes das faixas
df_assinantes['Faixa_Etaria'] = pd.cut(
    df_assinantes['Idade'], bins=bins, labels=labels, right=False)

# Exibindo as novas colunas e as primeiras linhas do DataFrame atualizado
print("\nDataFrame com novas colunas (primeiras 5 linhas):")
print(df_assinantes.head())

print("\nVerificando as faixas etárias criadas:")
print(df_assinantes['Faixa_Etaria'].value_counts().sort_index())

# --------------------------------------------------------------------------------

# Configurações para melhorar a aparência dos gráficos
# Um estilo de gráfico que se assemelha ao ggplot2 do R
plt.style.use('ggplot')
# Define uma paleta de cores para os gráficos do Seaborn
sns.set_palette('viridis')
# Define um tema com grade branca para os gráficos do Seaborn
sns.set_theme(style="whitegrid")

print("Estatísticas Descritivas das Variáveis Numéricas:")
print(df_assinantes.describe())

# Visualizando a distribuição da Idade
plt.figure(figsize=(10, 6))
sns.histplot(df_assinantes['Idade'], bins=10, kde=True)
plt.title('Distribuição de Idade dos Assinantes')
plt.xlabel('Idade')
plt.ylabel('Número de Assinantes')
plt.show()

# Visualizando a distribuição dos Meses Ativos
plt.figure(figsize=(10, 6))
sns.histplot(df_assinantes['Meses_Ativo'], bins=10, kde=True)
plt.title('Distribuição de Meses Ativos dos Assinantes')
plt.xlabel('Meses Ativos')
plt.ylabel('Número de Assinantes')
plt.show()

# Visualizando a distribuição da Receita Mensal (deve ser em torno dos valores dos planos)
plt.figure(figsize=(10, 6))
sns.histplot(df_assinantes['Receita_Mensal'], bins=5, kde=True)
plt.title('Distribuição da Receita Mensal por Assinante')
plt.xlabel('Receita Mensal (R$)')
plt.ylabel('Número de Assinantes')
plt.show()
