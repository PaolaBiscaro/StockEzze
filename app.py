import pandas as pd
import cv2
from pyzbar import pyzbar
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dash import Dash, dcc, html
import plotly.express as px
from flask import current_app
from datetime import datetime, date
# from your_application import app


app = Flask(__name__)


# Cria a instância do servidor Flask
# server = Flask(__name__)

# Cria a instância do aplicativo Dash
# app = Dash(__name__, server=server, url_base_pathname='/dashboard/')


# Configuração do banco de dados
db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": ""
}

# Função para conectar ao banco de dados


def conexao_bd():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Conexão com o MySQL foi bem-sucedida")
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    return connection


def excluir_registros_relacionados(produto_id):
    conexao = conexao_bd()
    cursor = conexao.cursor()

    sql_delete = "DELETE FROM lote WHERE produto_id = %s"
    cursor.execute(sql_delete, (produto_id,))

    # Commit para efetivar a exclusão
    conexao.commit()

    print("Registros relacionados excluídos com sucesso!")


# ID do produto que você deseja excluir
produto_id = 123  # Substitua pelo ID do produto que você quer excluir

# Chame a função para excluir os registros relacionados
excluir_registros_relacionados(produto_id)


def entrada_saida_produto(produto_id):
    conn = conexao_bd()
    cursor = conn.cursor()

    # Consulta para calcular a soma das entradas
    cursor.execute(
        'SELECT SUM(quantidade) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('entrada', produto_id))
    entrada_total = cursor.fetchone()[0] or 0

    # Consulta para calcular a soma das saídas
    cursor.execute(
        'SELECT SUM(quantidade) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('saida', produto_id))
    saida_total = cursor.fetchone()[0] or 0

    cursor.execute(
        'SELECT COUNT(*) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('entrada', produto_id))
    n_entrada = cursor.fetchone()[0] or 0

# Consulta para contar o número de registros de saída para um produto específico
    cursor.execute(
        'SELECT COUNT(*) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('saida', produto_id))
    n_saida = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return entrada_total, saida_total, n_entrada, n_saida


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/meuestoque')
def meu_estoque():
    conn = conexao_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produto')
    produtos = cursor.fetchall()

    cursor.execute('SELECT * FROM fornecedor')
    fornecedores = cursor.fetchall()

    entradas_saida_por_produto = {}
    for produto in produtos:
        produto_id = produto[0]
        
        cursor.execute(
            'SELECT SUM(quantidade) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('entrada', produto_id))
        n_entrada = cursor.fetchone()[0] or 0

        cursor.execute(
            'SELECT SUM(quantidade) FROM entradasaida WHERE tipo = %s AND produto_id = %s', ('saida', produto_id))
        n_saida = cursor.fetchone()[0] or 0

        entradas_saida_por_produto[produto_id] = {'entrada': n_entrada, 'saida': n_saida}

    cursor.execute(
        'SELECT lote.*, produto_id, estoque_minimo FROM lote JOIN produto ON lote.produto_id = produto_id')
    lotes = cursor.fetchall()

    cursor.close()
    conn.close()

    produto_id = produtos[0][0]

    lotes_por_produto = {}
    for lote in lotes:
        produto_id = lote[-1]
        if produto_id not in lotes_por_produto:
            lotes_por_produto[produto_id] = []
        lotes_por_produto[produto_id].append(lote)

    for lote_id, produtos_do_lote in lotes_por_produto.items():
        total_produtos = sum(produto[5] for produto in produtos_do_lote)
        lotes_por_produto[lote_id].append({'total_produtos': total_produtos})

    lotes_disponiveis = retirar_lote(produto_id)
    print(lotes_disponiveis)

    return render_template('estoqueprincipal.html', produtos=produtos, fornecedores=fornecedores, lotes=lotes, produto_id=produto_id, lotes_por_produto=lotes_por_produto, entradas_saida_por_produto=entradas_saida_por_produto, lotes_disponiveis=lotes_disponiveis)


@app.route('/retirar/<int:produto_id>', methods=['POST'])
def retirar(produto_id):
    print(produto_id)
    try:
        lote_id = request.form['lote']
        quantidade = int(request.form['quantidade'])

        conn = conexao_bd()
        cursor = conn.cursor()

        query = "UPDATE lote SET quantidade = GREATEST(quantidade - %s, 0) WHERE id = %s AND produto_id = %s"
        cursor.execute(query, (quantidade, lote_id, produto_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('meu_estoque'))
    except KeyError as e:
        return f"KeyError: {e}", 400


def retirar_lote(produto_id):
    conn = conexao_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM lote WHERE produto_id = %s', (produto_id,))
    lotes = cursor.fetchall()
    print(lotes)  # Adicione esta linha para verificar os lotes disponíveis

    cursor.close()
    conn.close()
    return lotes

@app.route('/lotes/<int:produto_id>')
def lotes_produto(produto_id):
    conn = conexao_bd()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM lote WHERE produto_id = %s"
    cursor.execute(query, (produto_id, ))

    id_produto_lote = cursor.fetchall()

    print(id_produto_lote)

    cursor.execute('SELECT * FROM produto')
    produtos = cursor.fetchall()
    
        # String de data
    data_string = '2024/06/11'

    # Converter a string para um objeto date
    data_date = datetime.strptime(data_string, '%Y/%m/%d').date()

    # Data atual para comparação
    data_atual = date.today()
    
    data_trinta = '2024/07/11'
    
    data_date_trinta = datetime.strptime(data_trinta, '%Y/%m/%d').date()

    # Comparar as datas
    if data_date > data_atual:
        print(f"A data {data_date} é maior que a data atual {data_atual}.")
    else:
        print(f"A data {data_date} não é maior que a data atual {data_atual}.")

        cursor.close()
        conn.close()

    return render_template('todoslotes.html', produto_id=produto_id, id_produto_lote=id_produto_lote, produtos=produtos, data_date=data_date, data_date_trinta=data_date_trinta)

# Filtrando os lotes próximos da validade


@app.route('/relatorio')
def relatorio():
    
    return render_template('relatorio.html')


@app.route('/adicionar', methods=['POST'])
def adicionar():
    produto_id = request.form['produto_id']
    quantidade = int(request.form['quantidade'])

    conn = conexao_bd()
    cursor = conn.cursor()

    query = "UPDATE produto SET quantidade = quantidade + %s WHERE id = %s"
    cursor.execute(query, (quantidade, produto_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('meu_estoque'))


# Rotas de Produto
@app.route('/cadastroproduto', methods=['GET', 'POST'])
@app.route('/editarproduto/<int:id>', methods=['GET', 'POST'])
def cadastro_ou_editar_produto(id=None):
    if id:
        # Se um ID de produto foi passado, é uma edição
        conexao = conexao_bd()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM produto WHERE id = %s', (id,))
        produto = cursor.fetchone()
        cursor.close()
        conexao.close()

        if produto is None:
            return "Produto não encontrado", 404
    else:
        produto = None

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        codigo = request.form['codigo']

        if id:  # Se um ID de produto foi passado, é uma edição
            conexao = conexao_bd()
            cursor = conexao.cursor()
            cursor.execute(
                'UPDATE produto SET nome = %s, descricao = %s, codigo = %s WHERE id = %s',
                (nome, descricao, codigo, id)
            )
        else:  # Se nenhum ID de produto foi passado, é um novo cadastro
            conexao = conexao_bd()
            cursor = conexao.cursor()
            cursor.execute(
                'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)',
                (nome, descricao, codigo)
            )

        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))

    return render_template('cadastro_produto.html', produto=produto)


@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    if request.form.get('_method') == 'DELETE':
        excluir_registros_relacionados(id)
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM produto WHERE id = %s', (id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))
    else:
        # Lidar com outras lógicas relacionadas ao método POST, se necessário
        pass


@app.route('/remover')
def remover_produto_estoque():
    return render_template('index.html')

# @app.route('/cadastroproduto', methods=['GET', 'POST'])
# def cadastro_produto():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         descricao = request.form['descricao']
#         codigo = request.form['codigo']
#         conexao = conexao_bd()
#         cursor = conexao.cursor()
#         cursor.execute(
#             'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)', (nome, descricao, codigo))
#         conexao.commit()
#         cursor.close()
#         conexao.close()
#         return redirect(url_for('meu_estoque'))
#     return render_template('cadastro_produto.html')


# @app.route('/editarproduto/<int:id>', methods=['GET', 'POST'])
# def editar_produto(id):
#     conexao = conexao_bd()
#     cursor = conexao.cursor(dictionary=True)
#     cursor.execute('SELECT  * FROM produto WHERE id = %s', (id,))
#     produto = cursor.fetchone()
#     cursor.close()
#     conexao.close()

#     if request.method == 'POST':
#         nome = request.form['nome']
#         descricao = request.form['descricao']
#         codigo = request.form['codigo']
#         conexao = conexao_bd()
#         pesquisa = conexao.cursor(dictionary=True)
#         pesquisa.execute(
#             'UPDATE produto SET nome = %s, descricao = %s, codigo = %s WHERE id = %s')
#         conexao.commit()
#         cursor.close()
#         conexao.close()
#         return redirect(url_for('meu_estoque'))

#     return render_template('cadastro_produto.html', produto=produto)


@app.route('/cadastrofornecedor', methods=['GET', 'POST'])
def cadastro_fornecedor():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        cnpj = request.form['cnpj']
        rua = request.form['rua']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']
        email = request.form['email']
        telefone = request.form['telefone']
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO fornecedor (nome, marca, cnpj, rua, bairro, cidade, estado, cep, email, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nome, marca, cnpj, rua, bairro, cidade, estado, cep, email, telefone))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))
    return render_template('cadastrofornecedor.html')


@app.route('/cadastrolote', methods=['GET', 'POST'])
def cadastro_lote():
    conn = conexao_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT id, nome FROM fornecedor')
    fornecedores = cursor.fetchall()

    cursor.execute('SELECT id, nome FROM produto')
    produtos = cursor.fetchall()

    if request.method == 'POST':
        
        codigo = request.form['codigo']
        #numero = request.form['numero']
        numero_padrao=1
        tipo_produto_padrao = 'tipo'
        valor_unitario = request.form['valor_unitario']
        valor_lote = request.form['valor_lote']
        quantidade = request.form['quantidade']
        estoque_minimo = request.form['estoque_minimo']
        data_cadastro = datetime.now().strftime('%Y-%m-%d')
        data_fabricacao = request.form['data_fabricacao']
        data_validade = request.form['data_validade']
        produto_id = request.form['produto_id']
        fornecedor_id = request.form['fornecedor_id']
        print(codigo, tipo_produto_padrao, valor_unitario, valor_lote, quantidade, estoque_minimo,
              data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id, numero_padrao)

        # Inserir o lote no banco de dados
        cursor.execute(
            'INSERT INTO lote (codigo, numero, tipo_produto, valor_unitario, valor_lote, quantidade, estoque_minimo, data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (codigo, numero_padrao, tipo_produto_padrao, valor_unitario, valor_lote, quantidade, estoque_minimo,
             data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id)
        )

        # Obter o ID do lote que acabou de ser inserido
        lote_id = cursor.lastrowid

        # Definir o usuário padrão para o registro na tabela entradasaida
        usuario_id_padrao = 1

        # Obter a data atual
        data_atual = datetime.now().strftime('%Y-%m-%d')

        # Inserir um registro na tabela entradasaida
        cursor.execute(
            'INSERT INTO entradasaida (tipo, data, quantidade, produto_id, lote_id, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)',
            ('entrada', data_atual, quantidade,
             produto_id, lote_id, usuario_id_padrao)
        )

        # Commit das alterações no banco de dados
        conn.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        # Redirecionar para a página de estoque após a inserção bem-sucedida
        return redirect(url_for('meu_estoque'))

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

    # Renderizar o template de cadastro de lote
    return render_template('cadastro_lote.html', fornecedores=fornecedores, produtos=produtos)



# @app.route('/leitorbarras')
# def leitor_barras():
#     return render_template('leitordebarras.html')


# def generate_frames():
#     cap = cv2.VideoCapture(0)
#     barcode_data = None
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             if barcode_data is None:
#                 # Decodifica os códigos de barras no quadro
#                 barcodes = pyzbar.decode(frame)
#                 for barcode in barcodes:
#                     # Extraia os dados do código de barras
#                     barcode_data = barcode.data.decode('utf-8')
#                     barcode_type = barcode.type

#                     # Desenhe um retângulo ao redor do código de barras
#                     (x, y, w, h) = barcode.rect
#                     cv2.rectangle(frame, (x, y), (x + w, y + h),
#                                   (0, 255, 0), 2)

#                     # Coloque o texto do código de barras na imagem
#                     text = "{} ({})".format(barcode_data, barcode_type)
#                     cv2.putText(frame, text, (x, y - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# # Print dos dados do código de barras
#                     print("Código de Barras Identificado:", barcode_data)
#             # Codificar o frame em formato de imagem JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Retornar o frame
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#             # Se um código de barras for identificado, pare de gerar novos quadros
#             if barcode_data is not None:
#                 opcao = str(input("Caso queira cadastrar o produto [S/N]"))
#                 if opcao == 'S':
#                     nome = str(input("Adicione o nome produto: "))
#                     descricao = str(input("Adicione a descrição: "))
#                     codigo = barcode_data
#                     conexao = conexao_bd()
#                     cursor = conexao.cursor()
#                     cursor.execute(
#                         'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)', (nome, descricao, codigo))
#                     conexao.commit()
#                     cursor.close()
#                     conexao.close()



# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario(): 
    conexao = conexao_bd()
    cursor = conexao.cursor()
    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto')
        descricao = request.form.get('descricao')
        codigo = codigo_b()  # Se codigo_b é uma função que você definiu em algum lugar
        print("form", codigo)
        cursor.execute(
            'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)', (nome_produto, descricao, codigo))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))
        


@app.route('/leitorbarras')
def leitor_barras():
    return render_template('leitordebarras.html')

def codigo_b():
    cap = cv2.VideoCapture(0)
    barcode_data = None
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if barcode_data is None:
                # Decodifica os códigos de barras no quadro
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    # Extraia os dados do código de barras
                    barcode_data = barcode.data.decode('utf-8')
                    # Print dos dados do código de barras
                    print("Código de Barras decodificado:", barcode_data)

            # Se um código de barras for identificado, pare de gerar novos quadros
            if barcode_data is not None:
                return barcode_data

def generate_frames():
    cap = cv2.VideoCapture(0)
    barcode_data = None
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if barcode_data is None:
                # Decodifica os códigos de barras no quadro
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    # Extraia os dados do código de barras
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type

                    # Desenhe um retângulo ao redor do código de barras
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)

                    # Coloque o texto do código de barras na imagem
                    text = "{} ({})".format(barcode_data, barcode_type)
                    cv2.putText(frame, text, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# Print dos dados do código de barras
                    
            # Codificar o frame em formato de imagem JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Retornar o frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Se um código de barras for identificado, pare de gerar novos quadros
            if barcode_data is not None:
                print("Apenas frames, pt1")
                break

                                                   



@app.route('/video_feed')
def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/leitorbarras')
# def leitor_barras():
#     return render_template('cadastro_produto_barra.html')


# # def generate_frames():
# #     cap = cv2.VideoCapture(0)
# #     barcode_data = None
# #     while True:
# #         success, frame = cap.read()
# #         if not success:
# #             break
# #         else:
# #             if barcode_data is None:
# #                 # Decodifica os códigos de barras no quadro
# #                 barcodes = pyzbar.decode(frame)
# #                 for barcode in barcodes:
# #                     # Extraia os dados do código de barras
# #                     barcode_data = barcode.data.decode('utf-8')
# #                     barcode_type = barcode.type

# #                     # Desenhe um retângulo ao redor do código de barras
# #                     (x, y, w, h) = barcode.rect
# #                     cv2.rectangle(frame, (x, y), (x + w, y + h),
# #                                   (0, 255, 0), 2)

# #                     # Coloque o texto do código de barras na imagem
# #                     text = "{} ({})".format(barcode_data, barcode_type)
# #                     cv2.putText(frame, text, (x, y - 10),
# #                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# #                     # Exibe um formulário HTML para o usuário preencher os detalhes do produto
# #                     conn = conexao_bd()
# #                     cursor = conn.cursor()
# #                     codigo_p = barcode_data
# #                     consulta = "SELECT * FROM produto WHERE codigo = %s"
# #                     cursor.execute(consulta, (codigo_p,))
# #                     resultado = cursor.fetchall()
# #                     cursor.close()
# #                     conn.close()
# #                     if len(resultado) > 0:
# #                         print("Produto encontrado:", resultado)
# #                     else:
# #                         print("Produto não encontrado no banco de dados.")
# #                         opcao = input("Deseja fazer um novo cadastro com o código de barras [S/N]? ")
# #                         if opcao.upper() == "S":
# #                             print("Redirecionando para cadastrar ou editar produto...")
# #                                     # Redirecionar para a rota de cadastro/editar produto
# #                             return cadastro_ou_editar_produto(id=None)
# #                         else:
# #                             print("Operação cancelada.")

# #                     # Retornar o frame
# #             yield (b'--frame\r\n'
# #                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def generate_frames():
#     cap = cv2.VideoCapture(0)
#     barcode_data = None
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             if barcode_data is None:
#                 # Decodifica os códigos de barras no quadro
#                 barcodes = pyzbar.decode(frame)
#                 for barcode in barcodes:
#                     # Extraia os dados do código de barras
#                     barcode_data = barcode.data.decode('utf-8')
#                     barcode_type = barcode.type

#                     # Desenhe um retângulo ao redor do código de barras
#                     (x, y, w, h) = barcode.rect
#                     cv2.rectangle(frame, (x, y), (x + w, y + h),
#                                   (0, 255, 0), 2)

#                     # Coloque o texto do código de barras na imagem
#                     text = "{} ({})".format(barcode_data, barcode_type)
#                     cv2.putText(frame, text, (x, y - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# # Print dos dados do código de barras
#                     print("Código de Barras Identificado:", barcode_data)
#             # Codificar o frame em formato de imagem JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Retornar o frame
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#             # Se um código de barras for identificado, pare de gerar novos quadros
#             if barcode_data is not None:

#                 print("Produto encontrado:", barcode_data)

#                 print("Produto não encontrado no banco de dados.")
#                 opcao = input(
#                     "Deseja fazer um novo cadastro com o código de barras [S/N]? ")
#                 if opcao.upper() == "S":
#                     print("Redirecionando para cadastrar produto...")
#                     # Redirecionar para a rota de cadastro de produto
#                     return redirect(url_for('cadastro_produto'))
#                 else:
#                     print("Operação cancelada.")
#                 break
 

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)

# @app.route('/leitorbarras')
# def leitor_barras():
#     return render_template('leitordebarras.html')


# def generate_frames():
#     cap = cv2.VideoCapture(0)
#     barcode_data = None
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             if barcode_data is None:
#                 # Decodifica os códigos de barras no quadro
#                 barcodes = pyzbar.decode(frame)
#                 for barcode in barcodes:
#                     # Extraia os dados do código de barras
#                     barcode_data = barcode.data.decode('utf-8')
#                     barcode_type = barcode.type

#                     # Desenhe um retângulo ao redor do código de barras
#                     (x, y, w, h) = barcode.rect
#                     cv2.rectangle(frame, (x, y), (x + w, y + h),
#                                   (0, 255, 0), 2)

#                     # Coloque o texto do código de barras na imagem
#                     text = "{} ({})".format(barcode_data, barcode_type)
#                     cv2.putText(frame, text, (x, y - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#                 if barcode_data is not None:
#                     break

# # Print dos dados do código de barras
#                 print("Código de Barras Identificado:", barcode_data)
#             # Codificar o frame em formato de imagem JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Retornar o frame
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#             # Se um código de barras for identificado, pare de gerar novos quadros
#             # if barcode_data is not None:
#             #     break
#  # Se um código de barras for identificado, pare de gerar novos quadros
#             if barcode_data is not None:
#                 conn = conexao_bd()
#                 cursor = conn.cursor()
#                 codigo_p = barcode_data
#                 consulta = "SELECT * FROM produto WHERE codigo = %s"
#                 cursor.execute(consulta, (codigo_p,))
#                 resultado = cursor.fetchall()
#                 if len(resultado) > 0:
#                     print("Produto encontrado:")

#                 else:
#                     opcao = str(
#                         input("Deseja fazer um novo cadastro com o código de barras [S/N]? "))
#                     if opcao == "S":
#                         print("Vá para cadastro de produtos")
#                         with current_app.app_context():
#                             return redirect(url_for('cadastro_ou_editar_produto'))

# def decode_barcodes(frame):
#     barcodes = pyzbar.decode(frame)
#     for barcode in barcodes:
#         barcode_data = barcode.data.decode('utf-8')
#         barcode_type = barcode.type
#         return barcode_data
#     return None

# def add_product_to_db(barcode, nome, descricao):
#     conn = conexao_bd()
#     cursor = conn.cursor()
#     query = "INSERT INTO produto (codigo, nome, descricao) VALUES (%s, %s, %s)"
#     cursor.execute(query, (barcode, nome, descricao))
#     conn.commit()
#     cursor.close()
#     conn.close()

# def processar_adicao_produto(barcode_data):
#     conn = conexao_bd()
#     cursor = conn.cursor()
#     consulta = "SELECT * FROM produto WHERE codigo = %s"
#     cursor.execute(consulta, (barcode_data,))
#     resultado = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     if len(resultado) > 0:
#         print("Produto encontrado:")
#     else:
#         # Redireciona para a rota de cadastro/edição de produto com o código de barras
#         return redirect(url_for('cadastro_ou_editar_produto', codigo=barcode_data))


# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# app.run(debug=True)
