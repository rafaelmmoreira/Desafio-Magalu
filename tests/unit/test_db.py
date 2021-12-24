from app import db
import redis


def test_db_vazio():
    """
    GIVEN bancos de clientes, favoritos e dados de autenticação
    WHEN ordenamos a limpeza dos bancos
    THEN os bancos devem ficar sem chaves
    """

    # Utilizando numeração diferente nos bancos para os testes!
    # Não seria minha opção favorita para um caso real...
    # Neste caso, seria preferível ter um servidor redis rodando em uma porta separada.
    # Para um projetinho "mock", parece mais inofensivo ter os bancos de teste e produção no mesmo servidor.
    db.banco = {
    'clientes':redis.Redis(encoding="utf-8", decode_responses=True, db=8),
    'favoritos':redis.Redis(encoding="utf-8", decode_responses=True, db=9),
    'auth':redis.Redis(encoding="utf-8", decode_responses=True, db=10),
    }

    db.banco['clientes'].flushdb()
    db.banco['favoritos'].flushdb()
    db.banco['auth'].flushdb()

    assert db.banco['clientes'].dbsize() == 0
    assert db.banco['favoritos'].dbsize() == 0
    assert db.banco['auth'].dbsize() == 0


def test_db_inserir_cliente():
    """
    GIVEN nome e email de um cliente
    WHEN inserimos os dados no banco
    THEN o nome fica mapeado ao email corretamente
    """
    db.criar_cliente('trajano@luizalabs.com.br', 'Luiza Trajano')
    db.criar_cliente('trajanojr@luizalabs.com.br', 'Fred Trajano')

    assert db.banco['clientes'].get('trajano@luizalabs.com.br') == 'Luiza Trajano'
    assert db.banco['clientes'].get('trajanojr@luizalabs.com.br') == 'Fred Trajano'

def test_db_atualizar_cliente():
    """
    GIVEN um e-mail de um cliente existente e um novo nome
    WHEN mandamos atualizar o cadastro do cliente no banco
    THEN o novo nome sobrescreve o antigo
    """
    db.banco['clientes'].set('trajanojr@luizalabs.com.br', 'Fred Trajano')
    db.atualizar_cliente('trajanojr@luizalabs.com.br', 'Frederico Trajano')

    assert db.banco['clientes'].get('trajanojr@luizalabs.com.br') == 'Frederico Trajano'

def test_db_remover_cliente():
    """
    GIVEN um e-mail de cliente já existene
    WHEN mandamos remover o cliente do banco
    THEN o e-mail deixa de ser uma chave válida no banco
    """
    db.banco['clientes'].set('trajanojr@luizalabs.com.br', 'Fred Trajano')

    db.deletar_cliente('trajanojr@luizalabs.com.br')

    assert db.banco['clientes'].get('trajanojr@luizalabs.com.br') == None
    
def test_db_inserir_produto():
    """
    GIVEN um e-mail de cliente e id de produto
    WHEN inserimos o produto no banco de favoritos
    THEN o produto entra em uma lista mapeada ao e-mail
    """
    db.banco['clientes'].set('trajano@luizalabs.com.br', 'Luiza Trajano')
    db.inserir_produto('trajano@luizalabs.com.br', 'produto123')
    db.inserir_produto('trajano@luizalabs.com.br', 'produto456')

    assert db.banco['favoritos'].lrange('trajano@luizalabs.com.br', 0, -1).sort() == ['produto123', 'produto456'].sort()

def test_db_inserir_produto_sem_cliente():
    """
    GIVEN um e-mail de cliente e id de produto
    WHEN inserimos o produto no banco de favoritos sem que o cliente esteja cadastrado
    THEN o produto não entra no banco de favoritos
    """
    db.inserir_produto('nao_existe@luizalabs.com.br', 'produto123')

    assert db.banco['favoritos'].lrange('nao_existe@luizalabs.com.br', 0, -1) == []

def test_db_inserir_produto_duplicado():
    """
    GIVEN um e-mail de cliente e id de produto
    WHEN o produto já existe no banco de favoritos
    THEN a duplicata do produto não será inserida
    """
    db.banco['clientes'].set('trajano@luizalabs.com.br', 'Luiza Trajano')
    db.inserir_produto('trajano@luizalabs.com.br', 'produto789')
    db.inserir_produto('trajano@luizalabs.com.br', 'produto789')

    assert db.banco['favoritos'].lrange('trajano@luizalabs.com.br', 0, -1).count('produto789') == 1

def test_visualizar_cliente():
    """
    GIVEN um e-mail de cliente 
    WHEN visualizamos o cliente
    THEN recebemos um objeto Cliente corretamente preenchido
    """
    db.banco['clientes'].set('trajano@luizalabs.com.br', 'Luiza Trajano')
    db.banco['favoritos'].lpush('trajano@luizalabs.com.br', '1bf0f365-fbdd-4e21-9786-da459d78dd1f')

    cliente = db.visualizar_cliente('trajano@luizalabs.com.br')

    assert cliente.nome == 'Luiza Trajano'
    assert cliente.email == 'trajano@luizalabs.com.br'   
    existe = False
    for produto in cliente.favoritos:
        if produto['id'] == '1bf0f365-fbdd-4e21-9786-da459d78dd1f':
            existe = True
    assert existe

def test_remover_produto():
    """
    GIVEN um e-mail de cliente e um id de produto
    WHEN removemos o produto dos favoritos do cliente
    THEN o produto realmente desaparece do banco de favoritos
    """
    db.banco['clientes'].set('trajano@luizalabs.com.br', 'Luiza Trajano')
    db.banco['favoritos'].lpush('trajano@luizalabs.com.br', 'bola de futebol')

    db.deletar_produto('trajano@luizalabs.com.br', 'bola de futebol')

    assert not 'bola de futebol' in db.banco['favoritos'].lrange('trajano@luizalabs.com.br', 0, -1)

'''
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
'''
