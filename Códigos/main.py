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

    # === MODIFICAÇÃO SUGERIDA AQUI ===
    # Aumentar a chance de cancelamento para o plano 'Básico'
    if plano_escolhido == 'Básico':
        status = np.random.choice(['Ativo', 'Cancelado'], p=[
                                  0.75, 0.25])  # 25% de chance de cancelar
    else:
        status = np.random.choice(['Ativo', 'Cancelado'], p=[
                                  0.90, 0.10])  # 10% de chance de cancelar
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

# Contagem de assinantes por Plano de Assinatura
plt.figure(figsize=(10, 6))
sns.countplot(data=df_assinantes, x='Plano_Assinatura',
              order=df_assinantes['Plano_Assinatura'].value_counts().index)
plt.title('Contagem de Assinantes por Plano de Assinatura')
plt.xlabel('Plano de Assinatura')
plt.ylabel('Número de Assinantes')
plt.show()

# Contagem de assinantes por Status de Assinatura
plt.figure(figsize=(8, 5))
sns.countplot(data=df_assinantes, x='Status_Assinatura')
plt.title('Status da Assinatura')
plt.xlabel('Status')
plt.ylabel('Número de Assinantes')
plt.show()

# Contagem de assinantes por Faixa Etária
plt.figure(figsize=(12, 6))
sns.countplot(data=df_assinantes, x='Faixa_Etaria',
              order=df_assinantes['Faixa_Etaria'].value_counts(sort=False).index)
plt.title('Contagem de Assinantes por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Número de Assinantes')
plt.show()

# Vendas (Custo_Total_Assinatura) por Localização - Top 10
vendas_por_localizacao = df_assinantes.groupby(
    'Localizacao')['Custo_Total_Assinatura'].sum().nlargest(10)
plt.figure(figsize=(12, 7))
sns.barplot(x=vendas_por_localizacao.index, y=vendas_por_localizacao.values)
plt.title('Custo Total de Assinatura (Receita) por Localização (Top 10)')
plt.xlabel('Localização (Estado)')
plt.ylabel('Custo Total de Assinatura (R$)')
# Rotaciona os rótulos do eixo X para melhor legibilidade
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de rótulos
plt.show()

# Criar uma coluna 'Ano_Mes_Registro' para agrupar
# O método to_period('M') converte para um período mensal, ideal para agrupamento temporal
df_assinantes['Ano_Mes_Registro'] = df_assinantes['Data_Registro'].dt.to_period(
    'M')

# 1. Contagem de novos registros por Ano e Mês
registros_mensais = df_assinantes.groupby(
    'Ano_Mes_Registro').size().reset_index(name='Num_Registros')
registros_mensais['Ano_Mes_Registro'] = registros_mensais['Ano_Mes_Registro'].astype(
    str)  # Converter para string para plotar

plt.figure(figsize=(15, 7))
sns.lineplot(data=registros_mensais, x='Ano_Mes_Registro',
             y='Num_Registros', marker='o')
plt.title('Número de Novos Registros de Assinantes por Mês')
plt.xlabel('Ano-Mês de Registro')
plt.ylabel('Número de Novos Assinantes')
plt.xticks(rotation=60, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Receita total gerada pelos novos assinantes por Ano e Mês (no momento do registro)
receita_mensal_registro = df_assinantes.groupby('Ano_Mes_Registro')[
    'Receita_Mensal'].sum().reset_index(name='Receita_Total_Registro')
receita_mensal_registro['Ano_Mes_Registro'] = receita_mensal_registro['Ano_Mes_Registro'].astype(
    str)

plt.figure(figsize=(15, 7))
sns.lineplot(data=receita_mensal_registro, x='Ano_Mes_Registro',
             y='Receita_Total_Registro', marker='o', color='green')
plt.title('Receita Total Gerada por Novos Assinantes por Mês')
plt.xlabel('Ano-Mês de Registro')
plt.ylabel('Receita Total (R$)')
plt.xticks(rotation=60, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# 1. Meses Ativos por Plano de Assinatura
plt.figure(figsize=(12, 7))
sns.boxplot(data=df_assinantes, x='Plano_Assinatura',
            y='Meses_Ativo', order=lista_planos)
plt.title('Meses Ativos por Plano de Assinatura')
plt.xlabel('Plano de Assinatura')
plt.ylabel('Meses Ativos')
plt.show()

# 2. Custo Total de Assinatura por Plano de Assinatura
plt.figure(figsize=(12, 7))
sns.barplot(data=df_assinantes, x='Plano_Assinatura',
            y='Custo_Total_Assinatura', estimator=sum, order=lista_planos)
plt.title('Custo Total de Assinatura (Receita) por Plano')
plt.xlabel('Plano de Assinatura')
plt.ylabel('Custo Total de Assinatura (R$)')
plt.show()

# 3. Meses Ativos por Status da Assinatura (para entender o churn)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_assinantes, x='Status_Assinatura', y='Meses_Ativo')
plt.title('Meses Ativos por Status da Assinatura')
plt.xlabel('Status da Assinatura')
plt.ylabel('Meses Ativos')
plt.show()

# Filtrar dados para assinantes cancelados e ativos para comparação
df_cancelados = df_assinantes[df_assinantes['Status_Assinatura'] == 'Cancelado']
df_ativos = df_assinantes[df_assinantes['Status_Assinatura'] == 'Ativo']

# 1. Distribuição de Planos entre Ativos vs. Cancelados
# Criar dois subplots lado a lado
fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

sns.countplot(data=df_ativos, x='Plano_Assinatura',
              order=lista_planos, ax=axes[0])
axes[0].set_title('Plano de Assinatura - Assinantes ATIVOS')
axes[0].set_xlabel('Plano de Assinatura')
axes[0].set_ylabel('Número de Assinantes')

sns.countplot(data=df_cancelados, x='Plano_Assinatura',
              order=lista_planos, ax=axes[1], color='salmon')
axes[1].set_title('Plano de Assinatura - Assinantes CANCELADOS')
axes[1].set_xlabel('Plano de Assinatura')
# axes[1].set_ylabel('Número de Assinantes') # Não precisa de rótulo no segundo, pois sharey=True

plt.tight_layout()
plt.show()

# 2. Distribuição de Faixa Etária entre Ativos vs. Cancelados
fig, axes = plt.subplots(1, 2, figsize=(18, 6), sharey=True)

sns.countplot(data=df_ativos, x='Faixa_Etaria',
              order=df_assinantes['Faixa_Etaria'].value_counts(sort=False).index, ax=axes[0])
axes[0].set_title('Faixa Etária - Assinantes ATIVOS')
axes[0].set_xlabel('Faixa Etária')
axes[0].set_ylabel('Número de Assinantes')

sns.countplot(data=df_cancelados, x='Faixa_Etaria', order=df_assinantes['Faixa_Etaria'].value_counts(
    sort=False).index, ax=axes[1], color='lightcoral')
axes[1].set_title('Faixa Etária - Assinantes CANCELADOS')
axes[1].set_xlabel('Faixa Etária')

plt.tight_layout()
plt.show()
