import sqlite3

connection = sqlite3.connect('library.db') #objeto que representa uma conecção com o bd
cursor = connection.cursor()#ponteiro responsavel por fazer operações na conexão estabelecida

cursor.execute("""
  CREATE TABLE usuario(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    cpf VARCHAR(11),
    email VARCHAR(255),
    telefone VARCHAR(14),
    login VARCHAR(255),
    senha VARCHAR(255)
  );

""")
print("Tabela usuario criada com sucesso")

cursor.execute("""
  CREATE TABLE livros(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(255),
    autor VARCHAR(255),
    ano_publicacao INTEGER,
    editora VARCHAR(255),
    tipo_livro VARCHAR(255),
    impresso BOOLEAN,
    localizacao VARCHAR(255)
  );

""")
print("Tabela livros criada com sucesso")

cursor.execute("""
  CREATE TABLE usuarioTemLivro(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    idLivro INTEGER,
    idUsuario INTEGER,
    FOREIGN KEY (idLivro) REFERENCES Livros(id),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id)
  );
""")
print("Tabela usuarioTemLivro criada com sucesso")
connection.commit()
connection.close()