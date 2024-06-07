from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# Função para criar a conexão com o banco de dados


def conexao_bd():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='paola05052015',
            database='stockezze_oficial'
        )
        if connection.is_connected():
            print("Conexão com o MySQL foi bem-sucedida")
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")

    return connection


@app.route('/meuestoque')
def meu_estoque():
    conn = conexao_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produto')
    produtos = cursor.fetchall()

    cursor.execute('SELECT * FROM fornecedor')
    fornecedores = cursor.fetchall()

    cursor.execute('SELECT lote.*, produto_id FROM lote JOIN produto ON lote.produto_id = produto_id')
    lotes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Passando o produto_id do primeiro produto da lista produtos
    produto_id = produtos[0][0]
    
    print(produtos)

    return render_template('estoqueprincipal.html', produtos=produtos, fornecedores=fornecedores, lotes=lotes, produto_id=produto_id)



@app.route('/leitorbarras')
def leitor_barras():
    return render_template("leitordebarras.html")


@app.route('/cadastroproduto')
def cadastro_produtos():
    return render_template("cadastrodeprodutos.html")


@app.route('/lotes/<int:produto_id>')
def lotes_produto(produto_id):
    # Conectar ao banco de dados
    conn = conexao_bd()
    cursor = conn.cursor(dictionary=True)

    #Executar a consulta
    
    query = "SELECT * FROM lote WHERE produto_id = %s"
    cursor.execute(query, (produto_id, ))

    id_produto_lote = cursor.fetchall()
    
    #ver a consulta sql
    formatted_query = query % produto_id
    print("Executando a consulta SQL: ", formatted_query)
    
    print(id_produto_lote)


    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Renderizar o template com os dados dos lotes
    return render_template('todoslotes.html', produto_id=produto_id, id_produto_lote=id_produto_lote)


@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


app.run(debug=True)
