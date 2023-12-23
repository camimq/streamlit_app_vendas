# Sobre o código do script

## [Dashboard.py](C:\Users\cqueiroz\OneDrive - Capgemini\Documents\2. docsCamila\repos2\streamlit_app_vendas\Dashboard.py)

### Função `formata_numero`

> Linhas 6 à 12

```
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'
```

A função `formata_numero` é responsável por formatar um valor numérico de acordo com um determinado padrão. Ela recebe dois parâmetros: valor, que é o número a ser formatado, e prefixo, que é um texto opcional a ser adicionado antes do número formatado.

A função utiliza um loop for para percorrer uma lista de unidades vazias e "mil". Dentro do loop, é verificado se o valor é menor que 1000. Se for, o número é formatado com duas casas decimais e a unidade vazia (caso seja o primeiro loop) ou a unidade "mil" (caso seja o segundo loop) é adicionada ao final. O número formatado é retornado.

Se o valor for maior ou igual a 1000, o valor é dividido por 1000 e o loop continua para a próxima unidade. Esse processo é repetido até que o valor seja menor que 1000. Nesse caso, o número é formatado com duas casas decimais e a unidade "milhões" é adicionada ao final. O número formatado é retornado.

Por exemplo, se chamarmos a função `formata_numero(1500, 'R$')`, o resultado será "R$ 1.50 mil". Se chamarmos a função `formata_numero(2500000)`, o resultado será "2.50 milhões".

#### Estrutura `for()`

É uma estrutura de repetição (ou _loop_) e que tem o mesmo princípio para qualquer linguagem de programação. Ou seja, uma vez entendido, é possível levar para qualquer linguagem existente até agora.

As estruturas de repetição são recursos das linguagens de progrmação responsáveis por executar um bloco de código repetidamente através de determinadas condições específicas.

O Python contém dois tipos de estruturas de repetição: `for` e `while`.

O `for` é utilizado para percorrer ou iterar sobre uma sequência de dados (seja uma lista, uma tupla, uma string), executando um conjunto de instruções em cada item.

Sua sintaxe básica é: `for<nome variável> in <iterável>`.

- `<nome variável>` é o nome da variável que vai receber os elementos de `<iterável>`
- `<iterável>` é o container de dados sobre o qual vamos iterar, podendo ser: uma lista, uma tupla, uma string, um dicionário entre outros.

**Exemplo:**
```
lista = [1, 2, 3, 4, 5]

for item in lista:
    print(item)
```

Passo a passo:

- Na primeira iteração, `item` vai receber o valor do primeiro elemento da lista `lista`, que é 1. Portanto `print(item)` vai mostrar o valor 1.

- Na segunda iteração, `item` vai receber o valor do segundo elemento da lista `lista`, que é 2. Portanto, `print(item)` vai mostrar valor 2.

- E assim por diante até o último valor que é 5. :smile:

##### Exemplos de loops com `for`

###### Listas

```
computador = ['Processador', 'Teclado', 'Mouse']

for item in computador:
    print(item)
```

**A saída será**

```
Processador
Teclado
Mouse
```

##### Dicionários

```
notas = {
    'Potuguês': 7, 
    'Matemática': 9, 
    'Lógica': 7, 
    'Algoritmo': 7
}

for chave, valor in notas.items():
    print(f"{chave}: {valor}")

```

**A saída será**

```
Potuguês: 7
Matemática: 9
Lógica: 7
Algoritmo: 7
```

> Retirado do artigo [**Loops e Estruturas de repetição no Python**](https://pythonacademy.com.br/blog/estruturas-de-repeticao)


### Transformando dados coletados de uma API em DataFrame

> Linha 21 do código

`dados = pd.DataFrame.from_dict(response.json())`

Esta parte do código usa o método `from_dict()` da classe `pd.DataFrame` da biblioteca pandas para criar um objeto DataFrame a partir de um dicionário.

O método `from_dict()` permite construir um DataFrame especificando os dados na forma de um dicionário, onde as chaves representam os nomes das colunas e os valores representam os dados de cada coluna.

Neste trecho de código específico, o método `response.json()` está retornando um dicionário, e o método `from_dict()` é usado para converter esse dicionário em um objeto DataFrame chamado dados.

### Tabelas

> Linhas 24 e 25

Este trecho de código está usando a biblioteca Pandas para manipular um conjunto de dados chamado `dados`. O objetivo é calcular a receita total por local de compra e, em seguida, associar essa informação com as coordenadas geográficas de cada local.

No primeiro comando, `receita_estados = dados.groupby('Local da compra')['Preço].sum()`, o código está agrupando os dados pleo campo `Local da compra` e somando os valores do campo `Preço` para cada grupo. Isso resultará em uma nova série Pandas onde o índice é o `Local da compra` e o valor é a soma dos preços, ou seja, a receita total para aquele local.

No segundo comando, `receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat','lon']].merge(receita_estados, left_on='Local da compra', right_index = True).sort_values('Preço', ascending=False)`, o código está realizando várias operações:

1. `dados.drop_duplicates(subset='Local da compra')`: remove as linhas duplicadas do DataFrame `dados` com base no campo `Local da compra`. Isso é feito para garantir que haja apenas uma linha para cada local de compra.

2. `[['Local da compra', 'lat', 'lon']]`: seleciona apenas as colunas `Local da compra`, `lat`, `lon` do DataFrame resultante.

3. `.merge(receita_estadosw, left_on = 'Local da compra, right_index = True)`: combina o DataFrame resultante com a série `receita_estados` com base no campo `Local da compra`. Isso adiciona a receita total calculada anteriormente como uma nova coluna no DataFrame.

4. `.sort_values('Preço', ascending=False)`: ordena o DataFrame resultante em ordem descrescente de `Preço`. Isso significa que os locais de compra com maior receita serão listados primeiro.

O resultado final é um Dataframe que contém o `Local da compra`, suas coordenadas geográficas (`lat` e `lon`) e a receita total para aquele local.


### Gráficos
> Linhas 35 a 44

Es trecho de código está usando a biblioteca Plotly Express para criar um gráfico de dispersão geográfica. O objetivo é visualizar a receita por estato em um mapa.

O comando `px.scatter_geo(receita_estados, lat = 'lat', lon = 'lon', scope = 'south america', size = 'Preço', template = 'seaborn', hover_name' = 'Local da compra', hover_data = {'lat' : False, 'lon' : False}, title='Receita por estado)` está criando o gráfico. Vamos entender cada parâmetro:

- `receita_estados`: é o DataFrame que contém os dados a serem plotados. Cada linha do DataFrame representa um ponto no gráfico.

- `lat = 'lat'` e `lon = 'lon'`: especificam as colunas do DataFram que contêm as coordenadas geográficas (latitude e longitude) de cada ponto.

- `scope = 'south america`: define o escopo do mapa para a América do Sul.

- `size = 'Preço`: define o tamanho de cada ponto com base nos valores da coluna 'Preço'. Isso significa que os pontos representando locais com maior receita serão maiores.

- `template = 'seaborn`: define o estilo visual do gráfico para Seaborn.

- `hover_name = 'Local da compra`: define a coluna do DataFrame que será exibida quando o usuário passar o mouse sobre um ponto.

- `hover_data={'lat' : False, 'lon' : Flase}`: espeficia quais dados adicionais serão exibidos quando o usuário passar o mouse sobre um ponto. Neste caso, as coordenadas geográficas não serão exibidas.

- `title = 'Receita por estado`: define o título do gráfico.

O resultado é um objeto `go.Figure` que representa o gráfico de dispersão geográfica. Este objeto pode ser exibido usando a função `show()` ou pode ser salvo como um arquivo usando a função `write_html()`.



### Ajusta o layout da aplicação

> Linhas 39 a 47

Esta parte do código cria um layout de painel com duas colunas usando a função `st.columns()` da biblioteca Streamlit.

A função `st.columns()` retorna uma lista de objetos de coluna que podem ser usados ​​para organizar o conteúdo do painel. Neste caso, está criando duas colunas, `coluna1` e coluna2, com largura igual.

A instrução with é então usada para especificar o bloco de código que será executado em cada coluna.

Dentro da `coluna1`, a função `st.metric()` é usada para exibir uma métrica no dashboard. São necessários dois argumentos: o rótulo ou título da métrica (`Receita total`) e o valor da métrica, que é calculado somando a coluna `Preço` do DataFrame `dados` usando `dados['Preço'].sum ()`.

Dentro da `coluna2`, outra função `st.metric()` é usada para exibir uma métrica diferente. Desta vez, mostra o rótulo `Quantidade de vendas` e o valor é obtido acessando o atributo `shape` do DataFrame `dados`, que retorna o número de linhas do DataFrame usando `dados.shape[0]`.