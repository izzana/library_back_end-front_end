from flask import Blueprint, jsonify, request


livros_routes = Blueprint("livros", __name__)
livro_dao

@livros_routes.route("/api/v1/livros", methods=["GET"])
def get_all_books():
    print("Method get all books")
    

@livros_routes.route("/api/v1/livros", methods=["PUT"])
def update():
    print("Method update book")
    
@livros_routes.route("/api/v1/livros", methods=["PUT"])
def update_by_id():
    print("Method update book")

@livros_routes.route("/api/v1/livros/<string:id>", methods=["DELETE"])
def remover():
    print("Method delete")


    