from app import app, db
import redis
import pytest

'''
Os testes automatizados se subdividem em duas partes:
1) Testes unitários, focados nos modelos (Cliente e Produto) e nas funcionalidades de banco de dados.
2) Testes de integração, que utilizam uma fixture pronta para realizar testes mais robustos fazendo
    requests HTTP direto para a aplicação e monitorando os resultados comportamentais.
'''

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    
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

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client