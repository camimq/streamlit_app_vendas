import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# configura de forma padrão, a exibição do streamlit
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
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox('Dados de todo o período', value = True)

if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)


query_string = {'regiao' : regiao.lower(), 'ano' : ano}
response = requests.get(url, params = query_string)
dados = pd.DataFrame.from_dict(response.json()) # Transforma os dados acessados em um DataFrame
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y') # altera o formato da coluna datas de string para datetime

filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]

## Tabelas
### Tabelas de receita
receita_estados = dados.groupby('Local da compra')['Preço'].sum() # agrupa os dados por Local de Compra e soma os valores de Preço
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending=False)


receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index() # Constroi tabela com Datetime
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year # constroi tabela com uma coluna com o mes e outra coluna com o ano
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name() # constroi tabela com uma coluna com o mes e outra coluna com o ano 

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

### Tabelas de quantidade de vendas

### Tabelas de vendedores
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))


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

fig_receita_estados = px.bar(receita_estados.head(),
                             x = 'Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top estados (receita)')
fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = px.bar(receita_categorias,
                                text_auto = True,
                                title = 'Receita por categoria')
fig_receita_categorias.update_layout(yaxis_title = 'Receita')

## Visualização no streamlit

# construção das abas de exibição
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

# construção dos gráficos na página Receita
with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

with aba3:
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores),
                                        x = 'sum',
                                        y = vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores),
                                        x = 'count',
                                        y = vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)
