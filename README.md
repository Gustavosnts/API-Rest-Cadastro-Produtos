# Documentação da API REST de Produtos

API Rest de cadastro de produtos, utilizando SLQlite, implementando CRUD, com front-end para consumir os serviços disponibilizados pela API, **projeto de cunho acadêmico**. 

## 1. Configuração da API

* **Tecnologias:** Python, HTML, CSS e bibliotecas Flask
* **Banco de Dados:** SQLite (`db-produtos.db`)
* **CORS:** Habilitado para permitir requisições (front-end).
* **URL Base:** `http://127.0.0.1:5000`

## 2. Endpoints

### 2.1. `/produtos`

* **Método:** `POST`
* **Descrição:** Cadastra um novo produto.

* **Método:** `GET`
* **Descrição:** Lista todos os produtos cadastrados.

### 2.2. `/produtos/<int:idproduto>`

* **Método:** `GET`
* **Descrição:** Exibe os detalhes de um produto específico pelo seu ID.

* **Método:** `PUT`
* **Descrição:** Atualiza os dados de um produto existente pelo seu ID.

* **Método:** `DELETE`
* **Descrição:** Exclui um produto pelo seu ID.

## 3. Tratamento de Erros

A API utiliza códigos de status HTTP para indicar o resultado de cada requisição. As respostas de erro geralmente incluem um objeto JSON com a chave `"erro"` contendo uma descrição do problema.

## 4. Como Executar a API

1.  Certifique-se de ter Python e a biblioteca Flask instalada (`pip install Flask Flask-CORS`).
2.  Salve o código da API em um arquivo Python (por exemplo, `app.py`).
3.  Crie um arquivo de banco de dados SQLite chamado `db-produtos.db` no mesmo diretório do `app.py` (ou ajuste o caminho na variável `DATABASE` do `app.py` conforme a sua estrutura de arquivos).
4.  Abra um terminal ou prompt de comando, navegue até o diretório onde você salvou o arquivo `app.py` e execute o comando: `python app.py`.
5.  A API estará rodando localmente no endereço `http://127.0.0.1:5000`.

## 5. Como Consumir a API (Exemplo com JavaScript no Front-end)

O front-end (arquivo `index.html`) fornecido demonstra como consumir essa API utilizando a função `fetch` do JavaScript para realizar as requisições HTTP para os diferentes endpoints. Certifique-se de que o seu arquivo `index.html` esteja no mesmo diretório (pasta) ou servido por um servidor web que possa acessar a API Flask.
