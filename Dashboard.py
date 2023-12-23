import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# configura de fomra padrão, a exibição do streamlit
st.set_page_config(layout = 'wide')

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
dados = pd.DataFrame.from_dict(response.json()) # Transforma os dados acessados em um DataFrame
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')   # altera o formato da coluna datas de string para datetime

# constroi tabela com date time

## Tabelas
receita_estados = dados.groupby('Local da compra')['Preço'].sum() # agrupa os dados por Local de Compra e soma os valores de Preço
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending=False)


receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index() # Constroi tabela com Datetime
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year # constroi tabela com uma coluna com o mes e outra coluna com o ano
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name()   # constroi tabela com uma coluna com o mes e outra coluna com o ano 

# Gráficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat', # especifica a col do DF que contem latitude
                                  lon = 'lon', # especifica a col do DF que contem longitude
                                  scope = 'south america', # define o scope do mapa para américa do sul
                                  size = 'Preço', # define o tamano dos pontos do mapa, baseado nos preços
                                  template = 'seaborn', # layout do gráfico no estilo Seaborn
                                  hover_name = 'Local da compra', # define a coluna Local da compra como info a ser exibida quando usuario passar o mouse sobre o ponto
                                  hover_data={'lat' : False, 'lon' : False}, # define dados que devem ser exibidos quando o usuário passar o mouse sobre o pontop; neste caso, NÃO serão exibidas as colunas lat e lon
                                  title = 'Receita por estado') # título do gráfico

fig_receita_mensal = px.line(receita_mensal, 
                             x = 'Mês',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita Mensal')
fig_receita_mensal.update_layout(yaxis_title = 'Receita')



## Visualização no streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapa_receita, use_container_width=True)
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
    st.plotly_chart(fig_receita_mensal, use_container_width=True)

st.dataframe(dados)
st.dataframe(receita_estados)
st.dataframe(receita_mensal)
