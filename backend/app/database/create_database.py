import sqlite3

connection = sqlite3.connect('library.db') #objeto que representa uma conecção com o bd
cursor = connection.cursor()#ponteiro responsavel por fazer operações na conexão estabelecida

cursor.execute("""
  CREATE TABLE Usuario (
    id IDENTITY PRIMARY KEY,
    nome VARCHAR(255),
    cpf VARCHAR(11),
    email VARCHAR(255),
    telefone VARCHAR(14),
    login VARCHAR(255),
    senha VARCHAR(255)
  );

""")
print("Tabela Usuario criada com sucesso")

cursor.execute("""
  CREATE TABLE livros(
    id IDENTITY PRIMARY KEY,
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
  CREATE TABLE UsuarioTemLivro(
    id IDENTITY PRIMARY KEY,
    idLivro INTEGER,
    idUsuario INTEGER,
    FOREIGN KEY (idLivro) REFERENCES Livros(id),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id)
  );
""")
print("Tabela UsuarioTemLivro criada com sucesso")
connection.commit()
connection.close()