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
qtd_vendas = dados.groupby('Local da compra')['Preço'].count()

### Tabelas de vendedores
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

# Gráficos

# Criação de um gráfico de dispersão geográfico para visualizar a quantidade de vendas por estado na América do Sul
# Utiliza a biblioteca Plotly Express para a criação do gráfico
fig_mapa_qtd_vendas = px.scatter_geo(qtd_vendas, # DataFrame contendo os dados de vendas
                                     lat = 'lat', # Coluna do DataFrame que contém as latitudes dos estados
                                     lon = 'lon', # Coluna do DataFrame que contém as longitudes dos estados
                                     scope = 'south america', # Limita o mapa para mostrar apenas a América do Sul
                                     size = 'Preço', # Utiliza a coluna 'Preço' para determinar o tamanho de cada ponto no mapa
                                     template = 'seaborn', # Define o estilo visual do gráfico como 'seaborn'
                                     title = 'Quantidade de vendas por estado') # Título do gráfico

# Criação de um gráfico de dispersão geográfico para visualizar a receita por estado na América do Sul
# Utiliza a biblioteca Plotly Express para a criação do gráfico
fig_mapa_receita = px.scatter_geo(receita_estados, # DataFrame contendo os dados de receita por estado
                                  lat = 'lat', # especifica a col do DF que contem latitude
                                  lon = 'lon', # especifica a col do DF que contem longitude
                                  scope = 'south america', # define o scope do mapa para américa do sul
                                  size = 'Preço', # define o tamano dos pontos do mapa, baseado nos preços
                                  template = 'seaborn', # layout do gráfico no estilo Seaborn
                                  hover_name = 'Local da compra', # define a coluna Local da compra como info a ser exibida quando usuario passar o mouse sobre o ponto
                                  hover_data={'lat' : False, 'lon' : False}, # define dados que devem ser exibidos quando o usuário passar o mouse sobre o pontop; neste caso, NÃO serão exibidas as colunas lat e lon
                                  title = 'Receita por estado') # título do gráfico

# Criação de um gráfico de linha para visualizar a evolução da receita mensal
# Utiliza a biblioteca Plotly Express para a criação do gráfico
fig_receita_mensal = px.line(receita_mensal, # DataFrame contendo os dados de receita mensal
                             x = 'Mês', # Define a coluna 'Mês' como eixo X, representando os meses
                             y = 'Preço', # Define a coluna 'Preço' como eixo Y, representando o valor da receita
                             markers = True, # Adiciona marcadores em cada ponto de dado no gráfico
                             range_y = (0, receita_mensal.max()), # Define o intervalo do eixo Y começando de 0 até o valor máximo de receita
                             color = 'Ano', # Diferencia as linhas por ano, usando cores diferentes
                             line_dash = 'Ano', # Aplica estilos de linha diferentes para cada ano
                             title = 'Receita Mensal') # Título do gráfico
fig_receita_mensal.update_layout(yaxis_title = 'Receita') # Atualiza o layout do gráfico para incluir um título no eixo Y

# Criação de um gráfico de barras para visualizar os estados com maior receita
# Utiliza a biblioteca Plotly Express para a criação do gráfico
fig_receita_estados = px.bar(receita_estados.head(), # Seleciona os primeiros registros do DataFrame 'receita_estados' para focar nos estados com maior receita
                             x = 'Local da compra', # Define a coluna 'Local da compra' como eixo X, representando os estados
                             y = 'Preço', # Define a coluna 'Preço' como eixo Y, representando o valor da receita em cada estado
                             text_auto = True, # Habilita a exibição automática do valor de 'Preço' em cada barra do gráfico
                             title = 'Top estados (receita)') # Título do gráfico
fig_receita_estados.update_layout(yaxis_title = 'Receita') # Atualiza o layout do gráfico para incluir um título no eixo Y, melhorando a clareza do gráfico

# Criação de um gráfico de barras para visualizar a receita por categoria
# Utiliza a biblioteca Plotly Express para a criação do gráfico
fig_receita_categorias = px.bar(receita_categorias, # DataFrame 'receita_categorias' contendo os dados de receita por categoria
                                text_auto = True, # Habilita a exibição automática dos valores de receita em cada barra do gráfico
                                title = 'Receita por categoria') # Título do gráfico
fig_receita_categorias.update_layout(yaxis_title = 'Receita') # Atualiza o layout do gráfico para incluir um título no eixo Y, especificando que o eixo representa a receita

## Visualização no streamlit

# construção das abas de exibição
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

# Construção do layout do dashboard com duas colunas utilizando Streamlit
with aba1:
    # Criação de duas colunas na interface do dashboard
    coluna1, coluna2 = st.columns(2)
    # Conteúdo da primeira coluna
    with coluna1:
        # Exibição da métrica de receita total com formatação em moeda
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
        # Gráfico de dispersão geográfico mostrando a receita por estado
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        # Gráfico de barras mostrando a receita por estado
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    
    # Conteúdo da segunda coluna
    with coluna2:
        # Exibição da métrica de quantidade total de vendas
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        # Gráfico de linha mostrando a evolução da receita mensal
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        # Gráfico de barras mostrando a receita por categoria
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

# Segmentação do dashboard em abas para melhor organização e visualização dos dados

# Aba 2: Visualização de métricas e gráficos relacionados à receita e vendas
with aba2:
    # Divisão da aba em duas colunas para distribuição dos componentes
    coluna1, coluna2 = st.columns(2)
    # Coluna 1: Foco em métricas e gráficos de receita
    with coluna1:
        # Exibição da receita total com formatação em moeda
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
         # Gráfico de dispersão geográfico mostrando a receita por estado
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        # Gráfico de barras mostrando os estados com maior receita
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    # Coluna 2: Foco em métricas e gráficos de quantidade de vendas
    with coluna2:
        # Exibição da quantidade total de vendas
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        # Gráfico de dispersão geográfico mostrando a quantidade de vendas por estado
        st.plotly_chart(fig_mapa_qtd_vendas, use_container_width=True)
        # Gráfico de barras mostrando a receita por categoria
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

# Aba 3: Visualização de métricas e gráficos relacionados aos vendedores
with aba3:
    # Input para seleção da quantidade de vendedores a serem exibidos nos gráficos
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)
    # Divisão da aba em duas colunas para distribuição dos componentes
    coluna1, coluna2 = st.columns(2)
    # Coluna 1: Gráfico de barras mostrando os vendedores com maior receita
    with coluna1:
        # Exibição da receita total com formatação em moeda
        st.metric('Receita total', formata_numero(dados['Preço'].sum(), 'R$'))
        # Criação e exibição do gráfico de barras para os vendedores com maior receita
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores),
                                        x = 'sum',
                                        y = vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)
        
    # Coluna 2: Gráfico de barras mostrando os vendedores com maior quantidade de vendas
    with coluna2:
        # Exibição da quantidade total de vendas
        # Utiliza a função st.metric para exibir a quantidade total de vendas. A quantidade é calculada
        # pela contagem de linhas no DataFrame 'dados' (dados.shape[0]). A função 'formata_numero' é
        # aplicada para formatar este número antes de exibi-lo.
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        # Criação e exibição do gráfico de barras para os vendedores com maior quantidade de vendas
        # Primeiro, seleciona os vendedores com maior quantidade de vendas ordenando o DataFrame 'vendedores'
        # pelo campo 'count' em ordem decrescente e pegando os primeiros 'qtd_vendedores'.
        # Depois, cria um gráfico de barras com Plotly Express (px.bar), onde o eixo x representa a contagem
        # de vendas ('count') e o eixo y usa os índices dos vendedores selecionados como rótulos.
        # O parâmetro 'text_auto=True' configura o gráfico para mostrar automaticamente os valores nas barras.
        # O título do gráfico inclui a quantidade de vendedores selecionados.
        # Por fim, o gráfico é exibido no dashboard com st.plotly_chart, ajustando-se à largura do contêiner.
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores), # Seleciona os vendedores com maior quantidade de vendas
                                        x = 'count',
                                        y = vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)
