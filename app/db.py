'''
Nota sobre o banco de dados:

O módulo SQLAlchemy é popularmente utilizado junto com o Flask para fazer interface com banco de dados.
Ele é bastante simples de usar, se integra com diferentes bancos comerciais e possui farta documentação
e e exemplos na internet.

Porém, dentre os bancos listados no enunciado do desafio, optei por utilizar o Redis justamente por ser
um banco NoSQL, o que foge um pouco do padrão que a maioria de nós acaba tendo contato em nossa formação
(bancos relacionais com SQL) e poderia demonstrar um pouco melhor minha capacidade de aprender algo novo.

Por conta disso, adotei o módulo mais popular para lidar com Redis em Python. 

Soluções com SQLAlchemy normalmente utilizam diversos modelos prontos, e a própria modelagem das classes
próprias de cada problema pode se beneficiar herdando modelos pré-existentes. "Perdi" esses modelos prontos
ao optar pelo Redis, mas como essa API não é tão complexa, não vejo tanto prejuizo em montar os modelos de
Cliente e Produto manualmente, bem como todas as funções de consulta. Em contrapartida, creio que a facilidade
de trabalhar com Redis até mesmo compense em alguns pontos essa troca.
'''

import redis
from app import models

'''
São utilizados 3 bancos diferentes, pois o Redis impõe limita a "mistura" de diferentes estruturas de dados.
Pela simplicidade do projeto, o próprio e-mail está servindo como id de cada usuário.

- db0: dicionários chave-valor mapeando e-mail e nome dos clientes
- db1: lista mapeando e-mail aos produtos favoritos
- db2: hash mapeando e-mail aos campos de autenticação (hash da senha, token e validade do token)
'''

banco = {
    'clientes':redis.Redis(encoding="utf-8", decode_responses=True, db=0),
    'favoritos':redis.Redis(encoding="utf-8", decode_responses=True, db=1),
    'auth':redis.Redis(encoding="utf-8", decode_responses=True, db=2),
    }

def criar_cliente(email, nome):
    return banco['clientes'].set(email, nome, nx=True)

def atualizar_cliente(email, nome):
    existe = banco['clientes'].exists(email)
    if existe:
        if banco['clientes'].set(email, nome):
            return models.Cliente(email, nome, banco['favoritos'].lrange(email, 0, -1))
    
    return existe

def deletar_cliente(email):
    if banco['clientes'].exists(email):
        nome = banco['clientes'].get(email)
        favoritos = banco['favoritos'].lrange(email, 0, -1)
        banco['clientes'].delete(email)
        banco['favoritos'].delete(email)
        banco['auth'].delete(email)
        return models.Cliente(email, nome, favoritos)
    

def inserir_produto(email, produto):
    existe_cliente = banco['clientes'].exists(email)
    if existe_cliente:
        favoritos = banco['favoritos'].lrange(email, 0, -1)
        if produto in favoritos:
            return None
        return banco['favoritos'].lpush(email, produto)    
    return existe_cliente

def visualizar_cliente(email):
    if banco['clientes'].exists(email):
        cliente = models.Cliente(email, banco['clientes'].get(email), banco['favoritos'].lrange(email, 0, -1))
        return cliente
    return None

def deletar_produto(email, produto):
    if banco['clientes'].exists(email):
        return banco['favoritos'].lrem(email, 0, produto)
    else:
        return None

def buscar_hash(email):
    hash = banco['auth'].hget(email, 'hash')
    return hash

def salvar_hash(email, hash):
    banco['auth'].hset(email, 'hash', hash)

def buscar_token(email):
    token = banco['auth'].hget(email, 'token')
    validade = banco['auth'].hget(email, 'validade')
    if token and validade:
        return {'token':token, 'validade':validade}
    return None

def salvar_token(email, token, validade):
    banco['auth'].hset(email, 'token', token)
    banco['auth'].hset(email, 'validade', validade)

def alterar_validade_token(email, validade):
    banco['auth'].hset(email, 'validade', validade)