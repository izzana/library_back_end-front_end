import sqlite3

class LivrosDao:
    def connect(self): 
        self.conn = sqlite3.connect('../../library.db') 
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    def save(self, livro):
        params = [livro['titulo'], livro['autor'], livro['ano_publicacao'] , livro['editora'] , livro['tipo_livro'], livro['impresso'], livro['localizacao']]
        self.connect()
        result = self.cursor.execute("""
                      INSERT INTO livros (titulo, autor, ano_publicacao, editora, tipo_livro, impresso, localizacao) VALUES (?,?,?,?,?,?,?)
                  """, params) 
        modified_registers = result.rowcount 
        self.conn.commit() 
        self.disconnect()
        return modified_registers
    
    def get_all(self):
        self.connect()
        self.cursor.execute("""
          SELECT * FROM livros
        """)

        livros = self.cursor.fetchall()
        self.disconnect()
        return livros
    
    def get_livro_by_autor(self, autor):#tá certim
        self.connect()
        self.cursor.execute("""
          SELECT * FROM livros
          WHERE autor like ?
        """, (autor,))

        livro = self.cursor.fetchone()
        self.disconnect()
        return livro
    
    def update(self, user):
        params = [user['nome'], user['email'], user['telefone'], user['login'], user['senha'], user['id']]
        self.connect()
        result = self.cursor.execute("""
                      UPDATE usuario 
                      SET nome = ?, 
                      email = ?, 
                      telefone = ?,
                      login = ?, 
                      senha = ?
                      WHERE id = ?;
                  """, params) 
        modified_registers = result.rowcount 
        self.conn.commit() 
        self.disconnect()
        return modified_registers