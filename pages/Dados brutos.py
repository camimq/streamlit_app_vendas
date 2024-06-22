# Importações necessárias para o script "Dados brutos.py"

# streamlit: Usado para criar e gerenciar a interface web do aplicativo. Permite a construção de páginas web interativas
# de forma rápida e com poucas linhas de código.
import streamlit as st
# requests: Biblioteca para realizar requisições HTTP de forma simples e elegante. Utilizada para acessar e consumir dados
# de APIs ou outros serviços web.
import requests
# pandas: Biblioteca essencial para análise e manipulação de dados em Python. Oferece estruturas de dados poderosas e
# flexíveis, como DataFrames, facilitando a manipulação, análise e visualização de dados.
import pandas as pd
# time: Módulo que fornece funções relacionadas ao tempo, como pausas na execução do código (sleep) e medição de
# intervalos de tempo. Pode ser usado para lidar com limites de taxa de API ou para adicionar atrasos intencionais.
import time

# Função para converter um DataFrame em CSV
@st.cache_data # Decorador do Streamlit para cacheamento de dados. Melhora a performance ao evitar recalculos desnecessários.
def converte_csv(df):
    # Converte o DataFrame para CSV, sem incluir o índice do DataFrame no arquivo CSV.
    # Codifica o resultado em UTF-8 para garantir compatibilidade com diferentes sistemas e idiomas.
    return df.to_csv(index = False).encode('UTF-8')

# Função para exibir uma mensagem de sucesso temporária na interface web
def mensagem_sucesso():
    # Cria e exibe a mensagem de sucesso com um ícone de verificação. A variável `sucesso` armazena o objeto retornado por `st.success`.
    sucesso = st.success('Arquivo baixado com sucesso!', icon = "✅")
    # Pausa a execução do script por 5 segundos, mantendo a mensagem de sucesso visível na interface durante esse tempo.
    time.sleep(5)
    # Remove a mensagem de sucesso da interface, tornando o espaço que ela ocupava disponível para outros conteúdos.
    sucesso.empty()

st.title('DADOS BRUTOS')

# Obtenção e processamento de dados de produtos de uma API

# Define a URL da API que contém os dados dos produtos.
url = 'https://labdados.com/produtos'

# Realiza uma requisição GET para a URL especificada. A função `requests.get` é usada para obter os dados da API.
# O objeto `response` armazena a resposta da requisição.
response = requests.get(url)
# Converte a resposta JSON da API em um DataFrame do pandas. A função `pd.DataFrame.from_dict` é utilizada para
# transformar os dados JSON em uma estrutura de DataFrame, facilitando a manipulação e análise dos dados.
dados = pd.DataFrame.from_dict(response.json())
# Converte a coluna 'Data da Compra' do DataFrame para o formato datetime, permitindo manipulações baseadas em data.
# A função `pd.to_datetime` é usada para converter as strings de data no formato '%d/%m/%Y' para o tipo datetime do pandas.
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

# Criação de um seletor de colunas na interface web

# Utiliza o componente `expander` do Streamlit para criar uma seção expansível na interface web. 
# Isso permite organizar melhor a interface e oferecer uma experiência de usuário mais limpa, 
# especialmente quando há muitas opções ou informações a serem apresentadas.
with st.expander('Colunas'):
    # Dentro do expander, cria um seletor múltiplo (`multiselect`) que permite ao usuário selecionar uma ou mais colunas 
    # de um DataFrame. O título do seletor é 'Selecione as colunas', e as opções disponíveis são as colunas do DataFrame `dados`.
    # Por padrão, todas as colunas são selecionadas, como indicado pelo segundo argumento `list(dados.columns)`, 
    # que também é usado como valor padrão para a seleção.
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')

# Criação de filtros na barra lateral para seleção de produtos, preço e data de compra

# Utiliza o componente `expander` na barra lateral (`st.sidebar`) para criar uma seção expansível intitulada 'Nome do produto'.
# Dentro deste expander, um seletor múltiplo (`multiselect`) permite ao usuário selecionar um ou mais produtos da lista de produtos únicos disponíveis.
# A lista de produtos únicos é obtida através de `dados['Produto'].unique()`, e todos os produtos são selecionados por padrão.
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
# Cria outro expander na barra lateral para o filtro de preço. Dentro deste expander, um controle deslizante (`slider`) permite ao usuário
# selecionar um intervalo de preço, variando de 0 a 5000. O intervalo de seleção padrão é definido para o intervalo completo (0, 5000).
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
# Adiciona um terceiro expander na barra lateral para a seleção de data de compra. Dentro deste expander, um input de data (`date_input`)
# permite ao usuário selecionar um intervalo de datas. O intervalo disponível é definido com base na data mínima e máxima encontradas na coluna
# 'Data da Compra' do DataFrame `dados`.
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

# Filtragem e exibição de dados na interface web

# Define uma string de consulta (query) para filtrar o DataFrame `dados` com base em critérios selecionados pelo usuário:
# - `Produto in @produtos`: Filtra os dados para incluir apenas as linhas onde o valor da coluna 'Produto' está na lista `produtos`.
# - `@preco[0] <= Preço <= @preco[1]`: Filtra os dados para incluir apenas as linhas onde o valor da coluna 'Preço' está dentro do intervalo especificado por `preco`.
# - `@data_compra[0] <= `Data da Compra` <= @data_compra[1]`: Filtra os dados para incluir apenas as linhas onde a data da compra está dentro do intervalo especificado por `data_compra`.
query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''
# Utiliza a função `query` do pandas para aplicar a string de consulta ao DataFrame `dados`, resultando em um novo DataFrame `dados_filtrados` contendo apenas as linhas que atendem aos critérios de filtragem.
dados_filtrados = dados.query(query)
# Filtra as colunas de `dados_filtrados` para incluir apenas aquelas selecionadas pelo usuário na interface web.
dados_filtrados=dados_filtrados[colunas]
# Exibe o DataFrame filtrado na interface web usando `st.dataframe`.
st.dataframe(dados_filtrados)

# Utiliza `st.markdown` para exibir a quantidade de linhas e colunas do DataFrame filtrado, formatando os números com a cor azul.
st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')
# Solicita ao usuário que escreva um nome para o arquivo CSV a ser gerado a partir dos dados filtrados.
st.markdown('Escreva um nome para o arquivo')
# Divide a interface web em duas colunas para organizar os elementos de entrada e ação.
coluna1, coluna2 = st.columns(2)
# Na primeira coluna, cria um campo de entrada de texto para o nome do arquivo, com o rótulo oculto e um valor padrão 'dados'.
# O nome do arquivo é automaticamente complementado com a extensão '.csv'.
with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value = 'dados')
    nome_arquivo += '.csv'

# Na segunda coluna, cria um botão de download que, ao ser clicado, gera e baixa o arquivo CSV dos dados filtrados.
# O botão também aciona a função `mensagem_sucesso` para exibir uma mensagem temporária de sucesso.
with coluna2:
    # Cria um botão de download usando `st.download_button`. Este botão permite ao usuário baixar os dados filtrados em formato CSV.
    # 'Fazer o download da tabela em CSV': Texto exibido no botão.
    # data: O conteúdo do arquivo CSV, obtido pela função `converte_csv`, que converte o DataFrame `dados_filtrados` em uma string CSV codificada em UTF-8.
    # file_name: O nome do arquivo CSV a ser baixado, definido pela variável `nome_arquivo`.
    # mime: Tipo de mídia do arquivo, definido como 'text/csv' para indicar que o arquivo é um CSV.
    # on_click: Função a ser chamada quando o botão é clicado. Aqui, é usada a função `mensagem_sucesso` para exibir uma mensagem temporária de sucesso após o download.
    st.download_button('Fazer o download da tabela em CSV', data = converte_csv(dados_filtrados), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)