import pandas as pd
import json
import os
print(f"Diretório de trabalho atual: {os.getcwd()}")


def csv_para_array_de_objetos(nome_do_arquivo):
    """
    Lê um arquivo CSV e o transforma em uma array de objetos (dicionários Python).

    Args:
        caminho_do_arquivo (str): O caminho para o arquivo CSV.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma linha do CSV.
    """
    try:
        # Lê o arquivo CSV para um DataFrame do pandas
        df = pd.read_csv('assinantes.csv')

        # Converte o DataFrame em uma lista de dicionários (objetos)
        # orient='records' faz com que cada linha seja um dicionário
        array_de_objetos = df.to_dict(orient='records')

        return array_de_objetos

    except FileNotFoundError:
        print(f"Erro: O arquivo '{'assinantes.csv'}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None


# Nome do seu arquivo CSV
nome_do_arquivo = 'assinantes.csv'

# Chama a função para transformar o CSV em uma array de objetos
dados_transformados = csv_para_array_de_objetos('assinantes.csv')

if dados_transformados:
    print(
        f"Dados transformados com sucesso. Total de {len(dados_transformados)} objetos.")
    # Você pode imprimir os primeiros 5 objetos para verificar
    for i, obj in enumerate(dados_transformados[:5]):
        # Usando json.dumps para uma visualização mais formatada
        print(f"Objeto {i+1}: {json.dumps(obj, indent=2, ensure_ascii=False)}")

    # Exemplo de como acessar dados do primeiro objeto
    # print(f"\nExemplo de acesso ao primeiro objeto:")
    # if dados_transformados:
    #     primeiro_objeto = dados_transformados[0]
    #     for chave, valor in primeiro_objeto.items():
    #         print(f"  {chave}: {valor}")
