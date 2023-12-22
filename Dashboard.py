import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

# Acessa os dados de vendas à partir de uma API
url = 'https://labdados.com/produtos'
response = requests.get(url)

# Transforma o resultado da requisição em um json
# Esta parte do código usa o método from_dict() da classe pd.DataFrame da biblioteca pandas para criar um objeto DataFrame a partir de um dicionário.

# O método from_dict() permite construir um DataFrame especificando os dados na forma de um dicionário, onde as chaves representam os nomes das colunas e os valores representam os dados de cada coluna.

# Neste trecho de código específico, o método response.json() está retornando um dicionário, e o método from_dict() é usado para converter esse dicionário em um objeto DataFrame chamado dados.
dados = pd.DataFrame.from_dict(response.json())

# Adicionando métricas na aplicação
st.metric('Receita total', dados['Preço'].sum())
st.metric('Quantidade de vendas', dados.shape[0])

st.dataframe(dados)