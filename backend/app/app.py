from flask import Flask
from app.routes.usuario_routes import usuario_routes
from app.routes.livros_route import livros_routes
from app.routes.emprestimos_routes import emprestimos_routes

app = Flask(__name__)
app.register_blueprint(usuario_routes)
app.register_blueprint(livros_routes)
app.register_blueprint(emprestimos_routes)