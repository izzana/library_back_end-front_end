from flask import Flask
from app.routes.usuario_routes import usuario_routes

app = Flask(__name__)
app.register_blueprint(usuario_routes)
