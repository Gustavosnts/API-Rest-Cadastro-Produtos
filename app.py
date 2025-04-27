from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app)

DATABASE = 'db-produtos.db'

def conectar_db():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela():
    conn = conectar_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    idproduto INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    precocompra REAL NOT NULL
                )
            ''')
            conn.commit()
            print("Tabela 'produtos' criada com sucesso!")
        except Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            conn.close()

with app.app_context():
    criar_tabela()

@app.route('/produtos', methods=['POST'])
def cadastrar():
    data = request.get_json()
    descricao = data.get('descricao')
    precocompra = data.get('precocompra')

    if descricao and precocompra:
        conn = conectar_db()
        if conn:
            try:
                sql = ''' INSERT INTO produtos(descricao, precocompra) VALUES(?,?) '''
                cur = conn.cursor()
                cur.execute(sql, (descricao, precocompra))
                conn.commit()
                return jsonify({'mensagem': 'Produto cadastrado com sucesso!', 'id': cur.lastrowid}), 201
            except Error as e:
                conn.rollback()
                return jsonify({'erro': f'Erro ao cadastrar produto: {e}'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500
    else:
        return jsonify({'erro': 'Dados incompletos para o cadastro'}), 400

@app.route('/produtos', methods=['GET'])
def listar():
    conn = conectar_db()
    if conn:
        try:
            sql = '''SELECT idproduto, descricao, precocompra FROM produtos'''
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()
            produtos_lista = [dict(row) for row in registros]
            return jsonify(produtos_lista), 200
        except Error as e:
            return jsonify({'erro': f'Erro ao listar produtos: {e}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

@app.route('/produtos/<int:idproduto>', methods=['GET'])
def exibir(idproduto):
    conn = conectar_db()
    if conn:
        try:
            sql = ''' SELECT idproduto, descricao, precocompra FROM produtos WHERE idproduto=? '''
            cur = conn.cursor()
            cur.execute(sql, (idproduto,))
            registro = cur.fetchone()
            if registro:
                return jsonify(dict(registro)), 200
            else:
                return jsonify({'erro': f'Produto com ID {idproduto} não encontrado'}), 404
        except Error as e:
            return jsonify({'erro': f'Erro ao buscar produto: {e}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

@app.route('/produtos/<int:idproduto>', methods=['PUT'])
def alterar(idproduto):
    data = request.get_json()
    descricao = data.get('descricao')
    precocompra = data.get('precocompra')

    if descricao and precocompra:
        conn = conectar_db()
        if conn:
            try:
                sql = ''' UPDATE produtos SET descricao=?, precocompra=? WHERE idproduto=? '''
                cur = conn.cursor()
                cur.execute(sql, (descricao, precocompra, idproduto))
                conn.commit()
                if cur.rowcount > 0:
                    return jsonify({'mensagem': f'Produto com ID {idproduto} atualizado com sucesso!'}), 200
                else:
                    return jsonify({'erro': f'Produto com ID {idproduto} não encontrado para atualização'}), 404
            except Error as e:
                conn.rollback()
                return jsonify({'erro': f'Erro ao atualizar produto: {e}'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500
    else:
        return jsonify({'erro': 'Dados incompletos para a atualização'}), 400

@app.route('/produtos/<int:idproduto>', methods=['DELETE'])
def excluir(idproduto):
    conn = conectar_db()
    if conn:
        try:
            sql = ''' DELETE FROM produtos WHERE idproduto=? '''
            cur = conn.cursor()
            cur.execute(sql, (idproduto,))
            conn.commit()
            if cur.rowcount > 0:
                return jsonify({'mensagem': f'Produto com ID {idproduto} excluído com sucesso!'}), 200
            else:
                return jsonify({'erro': f'Produto com ID {idproduto} não encontrado'}), 404
        except Error as e:
            conn.rollback()
            return jsonify({'erro': f'Erro ao excluir produto: {e}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

if __name__ == '__main__':
    app.run(debug=True)