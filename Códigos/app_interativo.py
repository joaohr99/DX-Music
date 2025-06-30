import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker  # Para regenerar os dados se necessário

# --- 1. Geração de Dados Fictícios (Replicando Parte 1) ---
# Esta parte do código deve ser executada para que o DataFrame exista


@st.cache_data  # Cache para não recalcular os dados toda vez que a app atualizar
def gerar_dados_assinantes(num_assinantes=1000):
    fake = Faker('pt_BR')

    dados = {
        'ID_Assinante': [],
        'Nome': [],
        'Email': [],
        'Data_Registro': [],
        'Idade': [],
        'Localizacao': [],
        'Plano_Assinatura': [],
        'Status_Assinatura': [],
        'Meses_Ativo': [],
        'Receita_Mensal': []
    }

    planos = {
        'Básico': 19.90,
        'Premium': 29.90,
        'Família': 49.90
    }
    lista_planos = list(planos.keys())

    for i in range(num_assinantes):
        dados['ID_Assinante'].append(i + 1)
        dados['Nome'].append(fake.name())
        dados['Email'].append(fake.email())

        data_registro = fake.date_between(start_date='-3y', end_date='today')
    # Convertendo o objeto date padrão do Faker para um Timestamp do Pandas ANTES de adicionar à lista
        dados['Data_Registro'].append(pd.Timestamp(data_registro))

        dados['Idade'].append(np.random.randint(18, 65))
        dados['Localizacao'].append(fake.state_abbr())

        # Manter a geração de status sem viés de plano para este exemplo,
        # a menos que você queira reintroduzir a simulação de correlação.
        plano_escolhido = np.random.choice(lista_planos, p=[0.3, 0.5, 0.2])
        dados['Plano_Assinatura'].append(plano_escolhido)

        status = np.random.choice(['Ativo', 'Cancelado'], p=[0.85, 0.15])
        dados['Status_Assinatura'].append(status)

        if status == 'Cancelado':
            dados['Meses_Ativo'].append(np.random.randint(1, 18))
        else:
            dados['Meses_Ativo'].append(np.random.randint(1, 36))

        dados['Receita_Mensal'].append(planos[plano_escolhido])

    df = pd.DataFrame(dados)

    # Adicionar colunas da Parte 2
    df['Mes_Registro'] = df['Data_Registro'].dt.month
    df['Ano_Registro'] = df['Data_Registro'].dt.year
    df['Custo_Total_Assinatura'] = df['Meses_Ativo'] * df['Receita_Mensal']

    bins = [18, 25, 35, 45, 55, 65]
    labels = ['18-24', '25-34', '35-44', '45-54', '55-64']
    df['Faixa_Etaria'] = pd.cut(
        df['Idade'], bins=bins, labels=labels, right=False)

    return df


# Carrega/gera os dados. O @st.cache_data garante que não seja regerado toda vez.
df_assinantes = gerar_dados_assinantes()

# Configurações de estilo para os gráficos
plt.style.use('ggplot')
sns.set_palette('viridis')
sns.set_theme(style="whitegrid")

# --- Interface Streamlit ---
# Ajusta o layout da página para ser mais largo
st.set_page_config(layout="wide")
st.title('Dashboard de Análise de Assinantes TuneWave Stream 🎶')

st.write("Bem-vindo ao dashboard interativo da TuneWave Stream. Explore as distribuições dos nossos assinantes!")

# Opção para o usuário selecionar o tipo de gráfico
st.sidebar.header('Configurações do Gráfico')
tipo_grafico = st.sidebar.selectbox(
    'Escolha a variável para visualizar a distribuição:',
    ('Idade', 'Meses Ativos', 'Receita Mensal',
     'Plano de Assinatura', 'Status da Assinatura', 'Faixa Etária')
)

# Renderiza o gráfico com base na seleção do usuário
if tipo_grafico == 'Idade':
    st.header('Distribuição de Idade dos Assinantes')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_assinantes['Idade'], bins=10, kde=True, ax=ax)
    ax.set_xlabel('Idade')
    ax.set_ylabel('Número de Assinantes')
    st.pyplot(fig)  # Exibe o gráfico no Streamlit

elif tipo_grafico == 'Meses Ativos':
    st.header('Distribuição de Meses Ativos dos Assinantes')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_assinantes['Meses_Ativo'], bins=10, kde=True, ax=ax)
    ax.set_xlabel('Meses Ativos')
    ax.set_ylabel('Número de Assinantes')
    st.pyplot(fig)

elif tipo_grafico == 'Receita Mensal':
    st.header('Distribuição da Receita Mensal por Assinante')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_assinantes['Receita_Mensal'], bins=5, kde=True, ax=ax)
    ax.set_xlabel('Receita Mensal (R$)')
    ax.set_ylabel('Número de Assinantes')
    st.pyplot(fig)

elif tipo_grafico == 'Plano de Assinatura':
    st.header('Contagem de Assinantes por Plano de Assinatura')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df_assinantes, x='Plano_Assinatura',
                  order=df_assinantes['Plano_Assinatura'].value_counts().index, ax=ax)
    ax.set_xlabel('Plano de Assinatura')
    ax.set_ylabel('Número de Assinantes')
    st.pyplot(fig)

elif tipo_grafico == 'Status da Assinatura':
    st.header('Status da Assinatura')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df_assinantes, x='Status_Assinatura', ax=ax)
    ax.set_xlabel('Status')
    ax.set_ylabel('Número de Assinantes')
    st.pyplot(fig)

elif tipo_grafico == 'Faixa Etária':
    st.header('Contagem de Assinantes por Faixa Etária')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(data=df_assinantes, x='Faixa_Etaria',
                  order=df_assinantes['Faixa_Etaria'].value_counts(sort=False).index, ax=ax)
    ax.set_xlabel('Faixa Etária')
    ax.set_ylabel('Número de Assinantes')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Você pode adicionar mais seções e gráficos aqui, por exemplo, a tabela de dados
st.subheader('Dados Brutos (Primeiras 10 Linhas)')
st.dataframe(df_assinantes.head(10))

# Informações de resumo (opcional)
st.subheader('Estatísticas Descritivas')
st.write(df_assinantes.describe())
