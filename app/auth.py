from app import models
import base64
import json
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

'''
Para autenticação e autorização, foi adotado um modelo simples utilizando token.

- Quando o usuário é cadastrado, é gerado um hash a partir de sua senha. O hash é armazenado no banco.
- Quando o usuário pede para se autenticar, o hash da senha fornecida é comparado com o do banco e um token é gerado.
- O token e seu prazo de validade (aqui foi adotado 1 dia) são armazenados no banco.
- Em todos os requests (exceto login), o processamento só ocorre se o token fornecido for válido e idêntico ao
  token armazenado no banco (usuário A não consegue visualizar/alterar usuário B por conta dos tokens diferentes).
'''


def verificar_senha(email, senha):
    hash = models.db.buscar_hash(email)
    return check_password_hash(hash, senha)

def salvar_senha(email, senha):
    hash = generate_password_hash(senha)
    models.db.salvar_hash(email, hash)


def obter_token(email, expires_in=3600):
    atual = datetime.utcnow()

    # busca o token atual no banco e testa sua validade
    token = models.db.buscar_token(email)
    if token and datetime.strptime(token['validade'], "%Y/%m/%d %H:%M:%S") > atual + timedelta(seconds=60):
        return json.dumps({'token':token['token']})

    # não encontrou/era inválido? gera token novo e salva no banco
    token = {}
    token['token'] = base64.b64encode(os.urandom(24)).decode('utf-8')
    token['validade'] = atual + timedelta(seconds=expires_in)
    models.db.salvar_token(email, token['token'], token['validade'].strftime("%Y/%m/%d %H:%M:%S"))
    return json.dumps({'token':token['token']}) 

def revogar_token(email):
    models.db.alterar_validade_token(datetime.utcnow() - timedelta(seconds=1))

def verificar_token(email, token):
    atual = datetime.utcnow()
    token_usuario = models.db.buscar_token(email)
    if token_usuario:
        if datetime.strptime(token_usuario['validade'], "%Y/%m/%d %H:%M:%S") > atual + timedelta(seconds=60) and \
        token_usuario['token'] == token:
            return True
    return False