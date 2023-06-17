import sqlite3
from datetime import datetime

class EmprestimosDao:
    def connect(self): 
        self.conn = sqlite3.connect('./app/database/library.db') 
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    def exists(self, id):
        self.connect()
        result = self.cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE id = ?", (id,))
        count = result.fetchone()[0]
        self.disconnect()
        return count > 0
    
    # def save(self, emprestimo):
    #     params = [emprestimo['id_livro'], emprestimo['id_usuario'], emprestimo['data_emprestimo'], emprestimo['data_devolucao']]
    #     self.connect()
    #     result = self.cursor.execute("""
    #                   INSERT INTO livros (titulo, autor, ano_publicacao, editora, tipo_livro, impresso, localizacao) VALUES (?,?,?,?,?,?,?)
    #               """, params) 
    #     modified_registers = result.rowcount 
    #     self.conn.commit() 
    #     self.disconnect()
    #     return modified_registers

    def save(self, emprestimo):
        try:
            self.connect()

            if 'data_devolucao' in emprestimo and emprestimo['data_devolucao']:
                # Se o campo 'data_devolucao' foi fornecido e não está vazio
                self.cursor.execute("""
                    INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao)
                    VALUES (?, ?, ?, ?)
                """, (emprestimo['id_livro'], emprestimo['id_usuario'], emprestimo['data_emprestimo'], emprestimo['data_devolucao']))
            else:
                # Se o campo 'data_devolucao' está vazio ou não foi fornecido
                self.cursor.execute("""
                    INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo)
                    VALUES (?, ?, ?)
                """, (emprestimo['id_livro'], emprestimo['id_usuario'], emprestimo['data_emprestimo']))

            self.conn.commit()

            # Atualize o campo 'emprestado' na tabela 'livros' para True
            self.cursor.execute("""
                UPDATE livros SET emprestado = 1 WHERE id = ?
            """, (emprestimo['id_livro'],))

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

        finally:
            self.disconnect()
    
    # def save_loan(self, id_livro, id_usuario, data_devolucao=None):
    #     data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #     emprestimo = {
    #         'id_livro': id_livro,
    #         'id_usuario': id_usuario,
    #         'data_emprestimo': data_emprestimo,
    #         'data_devolucao': data_devolucao
    #     }

    #     self.save(emprestimo)
    #     self.disconnect()

    # def save_loan(self, id_livro, id_usuario, data_devolucao=None):
    #     data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #     # Verificar se o livro já foi emprestado anteriormente
    #     self.connect()
    #     self.cursor.execute("""
    #         SELECT emprestado FROM livros WHERE id = ?
    #     """, (id_livro,))
    #     livro_emprestado = self.cursor.fetchone()

    #     if livro_emprestado and livro_emprestado[0] == 1:
    #         # O livro já foi emprestado, não é possível emprestar novamente
    #         self.disconnect()
    #         raise Exception("Livro já emprestado")

    #     emprestimo = {
    #         'id_livro': id_livro,
    #         'id_usuario': id_usuario,
    #         'data_emprestimo': data_emprestimo,
    #         'data_devolucao': data_devolucao
    #     }

    #     self.save(emprestimo)
    #     self.disconnect()
    
    def save_loan(self, id_livro, id_usuario, data_devolucao=None):
        data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Verificar se o livro existe
        self.connect()
        self.cursor.execute("""
            SELECT COUNT(*) FROM livros WHERE id = ?
        """, (id_livro,))
        livro_existe = self.cursor.fetchone()[0]

        if not livro_existe:
            # O livro não existe, lançar exceção ou retornar uma mensagem de erro
            self.disconnect()
            raise Exception("Livro não encontrado")

        # Verificar se o usuário existe
        self.cursor.execute("""
            SELECT COUNT(*) FROM usuario WHERE id = ?
        """, (id_usuario,))
        usuario_existe = self.cursor.fetchone()[0]

        if not usuario_existe:
            # O usuário não existe, lançar exceção ou retornar uma mensagem de erro
            self.disconnect()
            raise Exception("Usuário não encontrado")

        # Verificar se o livro já foi emprestado anteriormente
        self.cursor.execute("""
            SELECT emprestado FROM livros WHERE id = ?
        """, (id_livro,))
        livro_emprestado = self.cursor.fetchone()

        if livro_emprestado and livro_emprestado[0] == 1:
            # O livro já foi emprestado, não é possível emprestar novamente
            self.disconnect()
            raise Exception("Livro já emprestado")

        emprestimo = {
            'id_livro': id_livro,
            'id_usuario': id_usuario,
            'data_emprestimo': data_emprestimo,
            'data_devolucao': data_devolucao
        }

        self.save(emprestimo)
        self.disconnect()

    def return_book(self, id_emprestimo):
        try:
            self.connect()

            # Obtenha as informações do empréstimo pelo ID
            self.cursor.execute("""
                SELECT * FROM emprestimos WHERE id = ?
            """, (id_emprestimo,))

            emprestimo = self.cursor.fetchone()

            if not emprestimo:
                raise Exception("Empréstimo não encontrado.")

            # Verifique se já há uma data de devolução para o empréstimo
            if emprestimo[4]:
                raise Exception("Livro já foi devolvido.")
            # id_livro = emprestimo['id_livro']
            id_livro = emprestimo[1]
            # Atualize a data de devolução para a data atual
            data_devolucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                UPDATE emprestimos SET data_devolucao = ? WHERE id = ?
            """, (data_devolucao, id_emprestimo))

            # Atualize o campo 'emprestado' na tabela 'livros' para False
            self.cursor.execute("""
                UPDATE livros SET emprestado = 0 WHERE id = ?
            """, (id_livro,))

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

        finally:
            self.disconnect()

    def get_all(self):
        self.connect()
        self.cursor.execute("""
          SELECT * FROM emprestimos
        """)

        emprestimos = self.cursor.fetchall()
        self.disconnect()
        return emprestimos

    # def update(self, emprestimo):
    #     params = [emprestimo['data_devolucao'], emprestimo['id']]
    #     self.connect()
    #     result = self.cursor.execute("""
    #                 UPDATE emprestimos 
    #                 SET data_devolucao = ?, 
    #                 WHERE id = ?;
    #               """, params) 
    #     modified_registers = result.rowcount 
    #     self.conn.commit() 
    #     self.disconnect()
    #     return modified_registers
    
    # def update_emprestimo(self, emprestimo_id, data_devolucao):
    #   self.connect()
    #   self.conn.execute("BEGIN TRANSACTION")  # Inicia a transação

    #   # Verifica se o empréstimo está marcado como emprestado
    #   self.cursor.execute("""
    #       SELECT emprestimo, livro_id FROM emprestimos WHERE id = ?
    #   """, (emprestimo_id,))
    #   result = self.cursor.fetchone()
    #   if result is None:
    #       self.conn.execute("ROLLBACK")  # Cancela a transação
    #       self.disconnect()
    #       raise ValueError("Empréstimo não encontrado")

    #   emprestado, livro_id = result

    #   if not emprestado:  # Empréstimo está marcado como não emprestado
    #       # Atualiza o campo data_devolucao do empréstimo
    #       self.cursor.execute("""
    #           UPDATE emprestimos SET data_devolucao = ? WHERE id = ?
    #       """, (data_devolucao, emprestimo_id))

    #       # Atualiza o campo emprestimo do livro para True e define a data_emprestimo
    #       self.cursor.execute("""
    #           UPDATE livro SET emprestimo = 1, data_emprestimo = ? WHERE id = ?
    #       """, (data_devolucao, livro_id))

    #   else:  # Empréstimo já está marcado como emprestado
    #       # Atualiza o campo emprestimo do livro para False e remove a data_emprestimo
    #       self.cursor.execute("""
    #           UPDATE livro SET emprestimo = 0, data_emprestimo = NULL WHERE id = ?
    #       """, (livro_id,))

    #   self.conn.commit()  # Confirma a transação
    #   self.disconnect()

    # def update_emprestimo(self, emprestimo_id, data_devolucao=None):
    #     self.connect()
    #     self.conn.execute("BEGIN TRANSACTION")  # Inicia a transação

    #     # Verifica se o empréstimo está marcado como emprestado
    #     self.cursor.execute("""
    #         SELECT emprestimo, livro_id, data_emprestimo FROM emprestimos WHERE id = ?
    #     """, (emprestimo_id,))
    #     result = self.cursor.fetchone()
    #     if result is None:
    #         self.conn.execute("ROLLBACK")  # Cancela a transação
    #         self.disconnect()
    #         raise ValueError("Empréstimo não encontrado")

    #     emprestado, livro_id, data_emprestimo = result

    #     if not emprestado:  # Empréstimo está marcado como não emprestado
    #         if data_emprestimo is None:
    #             # Define a data_emprestimo como a data atual
    #             data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #             # Atualiza o campo emprestimo do livro para True e define a data_emprestimo
    #             self.cursor.execute("""
    #                 UPDATE livro SET emprestimo = 1, data_emprestimo = ? WHERE id = ?
    #             """, (data_emprestimo, livro_id))
    #         else:
    #             # Atualiza apenas o campo emprestimo do livro para True
    #             self.cursor.execute("""
    #                 UPDATE livro SET emprestimo = 1 WHERE id = ?
    #             """, (livro_id,))

    #     else:  # Empréstimo já está marcado como emprestado
    #         # Atualiza o campo emprestimo do livro para False e remove a data_emprestimo
    #         self.cursor.execute("""
    #             UPDATE livro SET emprestimo = 0, data_emprestimo = NULL WHERE id = ?
    #         """, (livro_id,))

    #         if data_devolucao is not None:
    #             # Atualiza o campo data_devolucao do empréstimo
    #             self.cursor.execute("""
    #                 UPDATE emprestimos SET data_devolucao = ? WHERE id = ?
    #             """, (data_devolucao, emprestimo_id))

    #     self.conn.commit()  # Confirma a transação
    #     self.disconnect()

    # def delete(self, id):
    #     params = [ id ]
    #     self.connect()
    #     result = self.cursor.execute("""
    #                   DELETE FROM livros 
    #                   WHERE id = ?;
    #               """, params) 
    #     modified_registers = result.rowcount 
    #     self.conn.commit() 
    #     self.disconnect()
    #     return modified_registers    