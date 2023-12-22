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

### Ajusta o layout da aplicação

> Linhas 20 a 27

Esta parte do código cria um layout de painel com duas colunas usando a função `st.columns()` da biblioteca Streamlit.

A função `st.columns()` retorna uma lista de objetos de coluna que podem ser usados ​​para organizar o conteúdo do painel. Neste caso, está criando duas colunas, `coluna1` e coluna2, com largura igual.

A instrução with é então usada para especificar o bloco de código que será executado em cada coluna.

Dentro da `coluna1`, a função `st.metric()` é usada para exibir uma métrica no dashboard. São necessários dois argumentos: o rótulo ou título da métrica (`Receita total`) e o valor da métrica, que é calculado somando a coluna `Preço` do DataFrame `dados` usando `dados['Preço'].sum ()`.

Dentro da `coluna2`, outra função `st.metric()` é usada para exibir uma métrica diferente. Desta vez, mostra o rótulo `Quantidade de vendas` e o valor é obtido acessando o atributo `shape` do DataFrame `dados`, que retorna o número de linhas do DataFrame usando `dados.shape[0]`.