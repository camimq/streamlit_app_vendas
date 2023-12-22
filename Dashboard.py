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

## Tabelas
receita_estados = dados.groupby('Local da compra')['Preço'].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending=False)

## Gráficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data={'lat' : False, 'lon' : False},
                                  title = 'Receita por estado')


## Visualização no streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapa_receita)
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

st.dataframe(dados)

#>

