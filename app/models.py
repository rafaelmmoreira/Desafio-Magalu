from app import db, auth
import requests
import json

class Cliente:
    def __init__(self, email, nome, favoritos=None):
        self.email = email
        self.nome = nome
        self.favoritos = []

        if not favoritos:
            favoritos = []

        for id in favoritos:
            produto = Produto.consulta_produto(id)
            if produto:
                self.favoritos.append(produto.dicionario())

    def json(self):
        dicionario = {}
        dicionario['nome'] = self.nome
        dicionario['email'] = self.email
        dicionario['favoritos'] = self.favoritos

        return json.dumps(dicionario)            


    @staticmethod
    def visualizar_cliente(email):
        cliente = db.visualizar_cliente(email)
        if cliente:
            return cliente
        return None

    @staticmethod
    def criar_cliente(email, nome, senha):        
        if db.criar_cliente(email, nome):
            auth.salvar_senha(email, senha)
            return Cliente(email, nome)
        
        return None
        
    @staticmethod
    def atualizar_cliente(email, nome):
        return db.atualizar_cliente(email, nome)      

    @staticmethod
    def deletar_cliente(email):
        return db.deletar_cliente(email)

    @staticmethod
    def inserir_favorito(email, id_produto):        
        return db.inserir_produto(email, id_produto)

    @staticmethod
    def deletar_favorito(email, id_produto):
        return db.deletar_produto(email, id_produto)



'''
Nota sobre a forma como a aplicação irá lidar com produtos:

Os produtos NÃO terão suas informações salvas em qualquer um dos bancos de dados ligados a esta API, 
exceto por seu id.

Todas as operações envolvendo produtos resultarão em um novo request para a API de produtos fornecida
no enunciado passando o id e recebendo todos os outros dados para exibição.

Apesar disso implicar uma provável quantidade mais elevada de requisições, isso evita inconsistências.
Por exemplo, o preço de um produto pode ter sido alterado ou novos reviews podem ter alterado seu score
médio.

Em um caso real, caso processamento fosse uma preocupação muito grande (e superior a armazenamento),
poderia-se discutir realizar a persistência dos dados completos do produto no banco vinculado a esta
API também e utilizar algum mecanismo de triggers para comunicar alterações no banco original e propagá-las
para este.
'''

class Produto:
    def __init__(self, id, title, price, image, review_score=None):
        self.id = id
        self.title = title
        self.price = price
        self.image = image
        self.review_score = review_score

    def dicionario(self):
        dic = {}
        dic['id'] = self.id
        dic['title'] = self.title
        dic['price'] = self.price
        dic['image'] = self.image
        if self.review_score:
            dic['reviewScore'] = self.review_score 
        return dic


    @staticmethod
    def consulta_produto(id):
        prod = requests.get('https://challenge-api.luizalabs.com/api/product/' + id + '/')
        if prod.status_code == 200:
            dicionario = prod.json()
            return Produto(dicionario['id'], dicionario['title'], dicionario['price'], dicionario['image'], dicionario.get('reviewScore'))
        else:
            return None
