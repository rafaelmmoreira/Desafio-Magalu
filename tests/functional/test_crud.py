import json
from app import db

def teste_criar_usuario(test_client):
    """
    GIVEN nome, email e senha válidos
    WHEN '/clientes' recebe um POST
    THEN a resposta é 201 e contém informações do cliente (exceto senha)
    """
    resposta = test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    assert resposta.status_code == 201
    assert b'Luiza Trajano' in resposta.data
    assert b'trajano@luizalabs.com.br' in resposta.data
    assert not (b'123456' in resposta.data)

def teste_criar_usuario_duplicado(test_client):
    """
    GIVEN informações de usuário já cadastrado
    WHEN '/clientes' recebe um POST
    THEN a resposta é proibido (403) e nenhuma informação do usuário é fornecida
    """
    resposta = test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    resposta = test_client.post('/clientes', json={'nome':'Tanto Faz', 'email':'trajano@luizalabs.com.br', 'senha':'abacate'})

    assert resposta.status_code == 403
    assert not (b'Luiza Trajano' in resposta.data)
    assert not (b'trajano@luizalabs.com.br' in resposta.data)
    assert not (b'123456' in resposta.data)

def teste_criar_usuario_invalido(test_client):
    """
    GIVEN informações de usuário incompletas
    WHEN '/clientes' recebe um POST
    THEN a resposta é 400
    """
    resposta = test_client.post('/clientes', json={'nome':'Tanto Faz', 'senha':'123456'})
    assert resposta.status_code == 400
    
    resposta = test_client.post('/clientes', json={'email':'tantofaz@luizalabs.com.br', 'senha':'abacate'})
    assert resposta.status_code == 400

    response = test_client.post('/clientes', json={'nome':'Tanto Faz', 'senha':'abacate'})
    assert resposta.status_code == 400    

def teste_visualizar_cliente(test_client):
    """
    GIVEN um usuário cadastrado
    WHEN '/clientes/<email>' recebe um GET
    THEN informações do usuário são retornadas se e somente se o usuário está autenticado 
    """
    test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    test_client.post('/clientes', json={'nome':'Fred Trajano', 'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})
    
    resposta = test_client.get('/clientes/trajano@luizalabs.com.br')
    assert resposta.status_code == 403
    resposta = test_client.get('/clientes/trajanojr@luizalabs.com.br')
    assert resposta.status_code == 403

    resposta = test_client.post('/auth', json={'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    assert resposta.status_code == 200
    token = json.loads(resposta.data)
    resposta = test_client.get('/clientes/trajano@luizalabs.com.br', json=token)
    assert resposta.status_code == 200
    assert b'Luiza Trajano' in resposta.data
    assert b'trajano@luizalabs.com.br' in resposta.data
    resposta = test_client.get('/clientes/trajanojr@luizalabs.com.br')
    assert resposta.status_code == 403

def teste_atualizar_cliente(test_client):
    """
    GIVEN um usuário cadastrado
    WHEN '/clientes/<email>' recebe um PUT com um novo nome
    THEN informações do usuário são retornadas se e somente se o usuário está autenticado 
    """
    test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    test_client.post('/clientes', json={'nome':'Fred Trajano', 'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})

    resposta = test_client.post('/auth', json={'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})
    assert resposta.status_code == 200
    token = json.loads(resposta.data)
    token['nome']='Frederico'

    resposta = test_client.put('/clientes/trajano@luizalabs.com.br', json=token)
    assert resposta.status_code == 403

    resposta = test_client.put('/clientes/trajanojr@luizalabs.com.br', json=token)
    assert resposta.status_code == 200

    assert b'Frederico' in resposta.data
    assert b'trajanojr@luizalabs.com.br' in resposta.data

def teste_manipular_favoritos(test_client):
    """
    GIVEN um usuário cadastrado
    WHEN '/clientes/<email>/favoritos' recebe um POST com um novo produto
    THEN o produto é inserido se e somente se o id do produto for válido, o produto for único e o usuário estiver autenticado 
    """

    test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    test_client.post('/clientes', json={'nome':'Fred Trajano', 'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})

    resposta = test_client.post('/auth', json={'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    assert resposta.status_code == 200
    token = json.loads(resposta.data)

    # Tentar inserir produto em outro usuário:
    resposta = test_client.post('/clientes/trajanojr@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', json=token)
    assert resposta.status_code == 403

    # Tentar inserir produto inválido
    resposta = test_client.post('/clientes/trajano@luizalabs.com.br/favoritos/1bf0f365-fbdd-ALFACE-9786-da459d78dd1f', json=token)
    assert resposta.status_code == 404

    # Produto válido:
    resposta = test_client.post('/clientes/trajano@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', json=token)
    assert resposta.status_code == 200

    # Produto duplicado:
    resposta = test_client.post('/clientes/trajano@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', json=token)
    assert resposta.status_code == 400

    resposta = test_client.get('/clientes/trajano@luizalabs.com.br', json=token)
    assert resposta.status_code == 200
    assert resposta.data.count(b'\"1bf0f365-fbdd-4e21-9786-da459d78dd1f\"') == 1

def teste_remover_favoritos(test_client):
    """
    GIVEN um usuário cadastrado
    WHEN '/clientes/<email>/favoritos' recebe um DELETE 
    THEN o produto é removido se e somente se ele existe e o usuário está autenticado
    """

    test_client.post('/clientes', json={'nome':'Luiza Trajano', 'email':'trajano@luizalabs.com.br', 'senha':'123456'})

    # senha inválida
    resposta = test_client.post('/clientes', json={'nome':'Fred Trajano', 'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})
    assert resposta.status_code == 403

    test_client.post('/clientes', json={'nome':'Fred Trajano', 'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})

    resposta = test_client.post('/auth', json={'email':'trajano@luizalabs.com.br', 'senha':'123456'})
    assert resposta.status_code == 200
    token_luiza = json.loads(resposta.data)

    resposta = test_client.post('/auth', json={'email':'trajanojr@luizalabs.com.br', 'senha':'qwerty'})
    assert resposta.status_code == 200
    token_fred = json.loads(resposta.data)

    resposta = test_client.post('/clientes/trajano@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', 
    json=token_luiza)

    resposta = test_client.post('/clientes/trajanojr@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', 
    json=token_fred)


    # token errado
    resposta = test_client.delete('/clientes/trajano@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', 
    json=token_fred)
    assert resposta.status_code == 403

    # produto inválido
    resposta = test_client.delete('/clientes/trajanojr@luizalabs.com.br/favoritos/1bf0f365-PIUI-ABACAXI-9786-da459d78dd1f', 
    json=token_fred)
    assert resposta.status_code == 404

    # agora vai
    resposta = test_client.delete('/clientes/trajanojr@luizalabs.com.br/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', 
    json=token_fred)
    assert resposta.status_code == 200

    resposta = test_client.get('/clientes/trajanojr@luizalabs.com.br', json=token_fred)
    assert resposta.status_code == 200
    assert not (b'1bf0f365-fbdd-4e21-9786-da459d78dd1f' in resposta.data)
