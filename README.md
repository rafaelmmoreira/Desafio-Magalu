# Desafio Magalu

## 1. Dependências e ferramentas

### 1.1 Linguagem Python
O projetinho foi inteiro desenvolvido em Python. A versão utilizada foi a 3.10, mas nenhuma feature específica desta versão foi utilizada, sendo seguro utilizar a versão 3.9 para testá-la.

Download: https://www.python.org/downloads/

### 1.2 Banco de dados Redis
O banco escolhido para realizar o projeto foi o Redis. A principal motivação foi fugir um pouco da "mesmice" dos bancos SQL e aprender algo de diferente.

No Ubuntu/Debian:
```
sudo apt-get install redis
```

Uma vez instalado, podemos fazer um _sanity check_ executando sua linha de comando:
```
redis-cli
```

Mantive as configurações padrão do banco de dados (porta 6379, sem senha). Caso esses parâmetros sejam alterados, será necessário alterar a inicialização do banco no arquivo ```db.py``` e também nos arquivos de testes.

### 1.3 Bibliotecas

A principal biblioteca utilizada foi o ```flask```, uma das bibliotecas mais conhecidas para gerenciar _backend_ em Python.
Além dela, foram utilizadas as bibliotecas ```redis-py``` para se conectar ao banco de dados, ```requests``` para fazer comunicação com a API fornecida e ```pytest``` para automação de testes unitários e de integração.

Instalação:
```
pip install flask
pip install requests
pip install redis
pip install pytest
```

# 2. Executando

## 2.1 Aplicação principal
Para executar a aplicação, basta navegar até a pasta do projeto e executar o comando
```
flask run
```
Isso irá inicializar o servidor e ele estará preparado para receber e responder às requisições.


## 2.2 Testes automatizados
Foi disponibilizado um conjunto de testes unitários testando os modelos criados (Cliente e Produto) e as principais funções de banco de dados, além de testes de integração que fazem sequências de requisições sob cenários diversos (inserções duplicadas, autenticação inválida, dados inválidos etc) e analisam seus resultados.
Os testes unitários não cobrem 100% das funções implementadas - o principal objetivo foi testar o "grosso" do trabalho feito e demonstrar o raciocínio desenvolvido. Para executá-los, ir até o diretório do projeto e:

```
python -m pytest
```

# 3. Rotas implementadas
As seguintes rotas foram implementadas:

| Rota                                          | Métodos          | Status Codes       | Descrição                                                                                                                                          | Dados necessários    |
|-----------------------------------------------|------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| ```/clientes```                                     | POST             | 201, 403           | Cria um cliente novo.                                                                                                                              | {nome, email, senha} |
| ```/clientes/<id_cliente>```                                | GET, PUT, DELETE | 200, 400, 403, 404 | Visualizar (nome, email e dados dos produtos favoritos), alterar o nome ou remover um cliente. Id é o e-mail. Exige autenticação.                  | {token, nome (put)}. |
| ```/clientes/<id_cliente>/favoritos/<id_produto>``` | POST, DELETE     | 200, 400, 403, 404 | Criar ou excluir um novo produto favorito. Exige autenticação. O produto é validado pela API de produtos fornecida pelo Magalu antes de ser salvo. | {token}              |
| ```/auth```                                         | POST             | 200, 403           | Autenticar. Valida a senha e gera um token a ser utilizado nas outras requisições.                                                                 | {email, senha}       |
  
 A resposta das requisições é sempre em JSON. Quando um recurso é manipulado com sucesso, seus dados voltam no JSON. Em caso de erro, o campo "mensagem" informa o erro. 
  
 # 4. Considerações sobre o projeto
 
Foram utilizadas diversas técnicas comuns a vários projetos semelhantes em Flask (como a modularização em rotas, modelos, banco de dados, autenticação e erros). Mas devido às dimensões e escopo limitados do projeto, tentei evitar o *overengineering* e em diversos pontos mantive as coisas relativamente simples (ex: o tratamento de erros ser implementado como uma única função no próprio arquivo de rotas, e a aplicação ser, de fato, uma única aplicação, dispensando o uso de *blueprints*).
  
A opção pelo Redis implica em abrir mão de facilidades do SQLAlchemy, o padrão *de facto* para trabalhar com banco de dados em projetos Flask, mas como parte do objetivo era demonstar minha capacidade de estudo, pareceu mais interessante partir para uma solução diferente. Além disso, acredito que a facilidade de uso do Redis "casou" bem com as necessidades e organização desse projeto.
  
Os dados dos produtos **não** são armazenados nos bancos de dados desta API. Ao acrescentar um produto novo, ele é validado através de uma requisição para a API de produtos do Magalu e apenas o seu ID é salvo. Ao requisitarmos informações sobre um usuário, os IDs de seus produtos favoritos são utilizados para fazer requisições novas para a API de produtos e obter as informações (preço, título, imagem e score) atualizadas. O motivo é garantir a consistência dos dados, evitando que o preço mude e o usuário veja o antigo, por exemplo. Em um ambiente real, seria possível discutir outras ferramentas para permitir uma integração melhor entre as APIs e facilitar o compartilhamento dessas mudanças sem a necessidade de fazer tantas requisições adicionais.

As ferramentas utilizadas aqui (principalmente o Flask e o Redis) são conhecidas por terem um bom desempenho ao serem executadas em um servidor dedicado. Naturalmente, seria possível melhorar ainda mais ao endereçar alguns potenciais gargalos - por exemplo, utilizando alguma forma assíncrona de fila de mensagens entre o banco e a aplicação, de modo que outras requisições possam começar a ser atendidas enquanto aguardamos o resultado de uma requisição anterior. Aqui entra o *mea culpa* do projetista que provavelmente precisaria avançar um pouco sobre o prazo do projeto e passar algumas horinhas do natal estudando e implementando a fila. :santa:

# 5. Considerações finais

Foi um projeto bastante divertido e estimulante! Agradeço a oportunidade de participar do desafio e espero ter produzido um resultado satisfatório para vocês!
