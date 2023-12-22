import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Formata números da aplicação
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

# Acessa os dados de vendas à partir de uma API
url = 'https://labdados.com/produtos'
response = requests.get(url)

# Transforma os dados acessados em um DataFrame
dados = pd.DataFrame.from_dict(response.json())

coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

st.dataframe(dados)