from app import models

"""
TESTES DE CLIENTE
"""

def test_novo_cliente():
    """
    GIVEN um modelo de Cliente
    WHEN um novo cliente é criado
    THEN email, nome e favoritos são definidos corretamente
    """
    cliente = models.Cliente('trajano@luizalabs.com.br', 'Luiza Trajano', ['1bf0f365-fbdd-4e21-9786-da459d78dd1f'])
    assert cliente.email == 'trajano@luizalabs.com.br'
    assert cliente.nome == 'Luiza Trajano'
    assert 'id' in cliente.favoritos[0]
    assert 'price' in cliente.favoritos[0]
    assert 'image' in cliente.favoritos[0]
    assert 'title' in cliente.favoritos[0]

def test_novo_cliente_sem_favs():
    """
    GIVEN um modelo de Cliente
    WHEN um novo cliente é criado sem produtos favoritos
    THEN email, nome e uma lista vazia de favoritos são definidos corretamente
    """
    cliente = models.Cliente('trajano@luizalabs.com.br', 'Luiza Trajano')
    assert cliente.email == 'trajano@luizalabs.com.br'
    assert cliente.nome == 'Luiza Trajano'
    assert cliente.favoritos == []

def test_novo_cliente_fav_invalido():
    """
    GIVEN um modelo de Cliente
    WHEN um novo cliente é criado com produtos favoritos inválidos
    THEN email, nome e uma lista favoritos omitindo os inválidos são definidos corretamente
    """
    cliente = models.Cliente('trajano@luizalabs.com.br', 'Luiza Trajano', ['1bf0f365-fbdd-BATATINHA-9786-da459d78dd1f'])
    assert cliente.email == 'trajano@luizalabs.com.br'
    assert cliente.nome == 'Luiza Trajano'
    assert cliente.favoritos == []



"""
TESTES DE PRODUTO
"""

def test_novo_produto():
    """
    GIVEN um modelo de Produto
    WHEN um novo produto é criado
    THEN seus campos id, price, image e review_score são definidos corretamente
    """
    produto = models.Produto('abc123', 'Emprego no Magalu', 'Não tem preço :)', 'smile.png', '5/5')
    assert produto.id == 'abc123'
    assert produto.title == 'Emprego no Magalu'
    assert produto.price == 'Não tem preço :)'
    assert produto.image == 'smile.png'
    assert produto.review_score == '5/5'

def test_novo_produto_sem_score():
    """
    GIVEN um modelo de Produto
    WHEN um novo produto é criado sem score
    THEN seus campos id, price, image e review_score (em branco) são definidos corretamente
    """
    produto = models.Produto('abc123', 'Emprego no Magalu', 'Não tem preço :)', 'smile.png')
    assert produto.id == 'abc123'
    assert produto.title == 'Emprego no Magalu'
    assert produto.price == 'Não tem preço :)'
    assert produto.image == 'smile.png'
    assert produto.review_score == None
