from flask import Flask, Blueprint, render_template, request
from mysql.connector import connect

# Conexão correta ao MySQL
conn = connect(
    host='127.0.0.1',
    database='stockezze_oficial',
    user='paola',
    password='paola'
)

# Usando o método cursor da conexão
cursor = conn.cursor()

    
    

usuario = Blueprint('usuario', __name__)

    
@usuario.route('/meuestoque')
def meu_estoque():
    # conn = conexao_db()
    # cursor = conn.cursor()
    # produtos = cursor.execute('SELECT * FROM Produto')
    # produtos = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return render_template('estoqueprincipal.html')
