from flask import Flask

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

from app import routes

