from app import app, models, auth
from flask import request
import json


@app.route('/clientes/<id>', methods=['GET'])
def visualizar_cliente(id):
    dados = request.get_json() or {}
    if 'token' in dados and auth.verificar_token(id, dados['token']):
        cliente = models.Cliente.visualizar_cliente(id)
        if cliente:
            return cliente.json(), 200
        return erro('Cliente não encontrado', 404)
    return erro('Você não possui permissão para visualizar', 403)

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    dados = request.get_json() or {}
    if 'nome' in dados and 'email' in dados and 'senha' in dados:
        cliente = models.Cliente.criar_cliente(dados['email'], dados['nome'], dados['senha'])
        if cliente:
            return cliente.json(), 201
        return erro('E-mail já cadastrado', 403)
    else:
        return erro('Dados incompletos', 400)

@app.route('/clientes/<id>', methods=['PUT'])
def atualizar_cliente(id):
    dados = request.get_json() or {}
    if 'token' in dados and auth.verificar_token(id, dados['token']):
        if 'nome' in dados:
            return models.Cliente.atualizar_cliente(id, dados['nome']).json(), 200
        else:
            return erro('dados incompletos', 400)
    return erro('Você não possui permissão para alterar', 403)

@app.route('/clientes/<id>', methods=['DELETE'])
def deletar_cliente(id):
    dados = request.get_json() or {}
    if 'token' in dados and auth.verificar_token(id, dados['token']):
        cliente = models.Cliente.deletar_cliente(id)
        if cliente:
            return cliente.json(), 200
    return erro('Você não tem permissão para excluir', 403)

@app.route('/clientes/<id_cliente>/favoritos/<id_produto>', methods=['POST'])
def inserir_favorito(id_cliente, id_produto):
    dados = request.get_json() or {}
    if 'token' in dados and auth.verificar_token(id_cliente, dados['token']):
        prod = models.Produto.consulta_produto(id_produto)
        if prod:
            if models.Cliente.inserir_favorito(id_cliente, id_produto):
                return json.dumps(prod.dicionario()), 200
            
            return erro('Produto repetido', 400)
        return erro('Produto não existe', 404)
    return erro('Você não possui permissão para inserir', 403)

@app.route('/clientes/<id_cliente>/favoritos/<id_produto>', methods=['DELETE'])
def deletar_favorito(id_cliente, id_produto):
    dados = request.get_json() or {}
    if 'token' in dados and auth.verificar_token(id_cliente, dados['token']):
        if models.Cliente.deletar_favorito(id_cliente, id_produto):
            return models.Cliente.visualizar_cliente(id_cliente).json(), 200        
        return erro('Produto não encontrado', 404)
    return erro('Você não possui permissão para remover', 403) 

@app.route('/auth', methods=['POST'])
def autenticar():
    dados = request.get_json() or {}
    if 'email' in dados and 'senha' in dados:
        if auth.verificar_senha(dados['email'], dados['senha']):
            return auth.obter_token(dados['email']), 200
    return erro('Usuário e/ou senha incorretos', 403)

def erro(mensagem, status):
    return {'erro':mensagem}, status