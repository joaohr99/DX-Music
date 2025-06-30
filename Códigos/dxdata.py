from faker import Faker
# ajuste o nome da função conforme necessário
from csv_para_array import *
from main import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ...existing code...

# Carregando os dados do CSV usando a função do csv_para_array.py
dados = carregar_dados_csv()  # ajuste se precisar passar o caminho do arquivo

# Se a função retorna um dicionário:
df_assinantes = pd.DataFrame(dados)

# Se já retorna um DataFrame, use diretamente:
# df_assinantes = dados

df_assinantes['Data_Registro'] = pd.to_datetime(df_assinantes['Data_Registro'])

# ...restante do código permanece igual...
