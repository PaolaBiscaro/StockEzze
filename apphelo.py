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

import pandas as pd

# Cria a instância do servidor Flask
# server = Flask(__name__)

# Cria a instância do aplicativo Dash
# app = Dash(__name__, server=server, url_base_pathname='/dashboard/')


app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Helo761.",
    "database": "stockezze_oficial"
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

    cursor.execute(
        'SELECT lote.*, produto_id, estoque_minimo FROM lote JOIN produto ON lote.produto_id = produto_id')
    lotes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Passando o produto_id do primeiro produto da lista produtos
    produto_id = produtos[0][0]

    print(produtos)

    lotes_por_produto = {}
    for lote in lotes:
        produto_id = lote[-1]  # Assumindo que produto_id é a última coluna
        if produto_id not in lotes_por_produto:
            lotes_por_produto[produto_id] = []
        lotes_por_produto[produto_id].append(lote)

    # Calculando o total de produtos em cada lote
    for lote_id, produtos_do_lote in lotes_por_produto.items():
        # Assumindo que a quantidade está na 5ª posição
        total_produtos = sum(produto[5] for produto in produtos_do_lote)
        lotes_por_produto[lote_id].append({'total_produtos': total_produtos})

    return render_template('estoqueprincipal.html', produtos=produtos, fornecedores=fornecedores, lotes=lotes, produto_id=produto_id, lotes_por_produto=lotes_por_produto)


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

    cursor.close()
    conn.close()

    return render_template('todoslotes.html', produto_id=produto_id, id_produto_lote=id_produto_lote, produtos=produtos)



@app.route('/relatorio')
def relatorio():
    # def obter_dados():
    #     conn = conexao_bd()

    #     query_faturamento_anual = '''
    #     SELECT YEAR(es.data) as Ano, SUM(es.quantidade * l.valor_unitario) as Faturamento_Anual
    #     FROM entradasaida es
    #     JOIN lote l ON es.lote_id = l.id
    #     WHERE es.tipo = 'saida'
    #     GROUP BY Ano
    #     ORDER BY Ano
    #     '''

    #     query_faturamento_mensal = '''
    #     SELECT YEAR(es.data) as Ano, MONTH(es.data) as Mes, SUM(es.quantidade * l.valor_unitario) as Faturamento_Mensal
    #     FROM entradasaida es
    #     JOIN lote l ON es.lote_id = l.id
    #     WHERE es.tipo = 'saida'
    #     GROUP BY Ano, Mes
    #     ORDER BY Ano, Mes
    #     '''

    #     query_total_produtos = 'SELECT COUNT(*) as Total_Produtos FROM produto'

    #     query_total_faturamento = '''
    #     SELECT SUM(es.quantidade * l.valor_unitario) as Faturamento_Total
    #     FROM entradasaida es
    #     JOIN lote l ON es.lote_id = l.id
    #     WHERE es.tipo = 'saida'
    #     '''

    #     df_anual = pd.read_sql(query_faturamento_anual, conn)
    #     df_mensal = pd.read_sql(query_faturamento_mensal, conn)
    #     df_total_produtos = pd.read_sql(query_total_produtos, conn)
    #     df_total_faturamento = pd.read_sql(query_total_faturamento, conn)

    #     conn.close()

    #     return df_anual, df_mensal, df_total_produtos.iloc[0]['Total_Produtos'], df_total_faturamento.iloc[0]['Faturamento_Total']

    # def relatorio():
    #     df_anual, df_mensal, total_produtos, total_faturamento = obter_dados()

    #     return render_template('relatorio.html',
    #                            total_produtos=total_produtos,
    #                            total_faturamento=total_faturamento,
    #                            df_anual=df_anual.to_html(
    #                                classes='table table-striped'),
    #                            df_mensal=df_mensal.to_html(classes='table table-striped'))

    # # Configuração do Dash
    # #app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

    # # Obter os dados para Dash
    # df_anual, df_mensal, total_produtos, total_faturamento = obter_dados()

    # # Gráfico de Faturamento Anual
    # fig_anual = px.bar(df_anual, x='Ano', y='Faturamento_Anual',
    #                    title='Faturamento Anual')

    # # Gráfico de Faturamento Mensal
    # fig_mensal = px.bar(df_mensal, x='Mes', y='Faturamento_Mensal',
    #                     color='Ano', title='Faturamento Mensal', barmode='group')

    # # Layout do Dash
    # app.layout = html.Div(children=[
    #     html.H1(children='Dashboard de Faturamento'),

    #     html.Div(children=[
    #         html.Div(children=f'Total de Produtos: {total_produtos}', style={
    #             'padding': 40,
    #             'fontSize': 25,
    #             'border': '2px solid black',
    #             'borderRadius': 5,
    #         }),
    #         html.Div(children=f'Faturamento Total: R$ {total_faturamento:,.2f}', style={
    #             'padding': 40,
    #             'fontSize': 25,
    #             'border': '2px solid black',
    #             'borderRadius': 5,
    #         }),
    #     ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    #     dcc.Graph(id='faturamento-anual', figure=fig_anual),
    #     dcc.Graph(id='faturamento-mensal', figure=fig_mensal)
    # ])

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


@app.route('/retirar', methods=['POST'])
def retirar():
    produto_id = request.form['produto_id']
    quantidade = int(request.form['quantidade'])

    conn = conexao_bd()
    cursor = conn.cursor()

    query = "UPDATE produto SET quantidade = GREATEST(quantidade - %s, 0) WHERE id = %s"
    cursor.execute(query, (quantidade, produto_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('meu_estoque'))


@app.route('/cadastroproduto', methods=['GET', 'POST'])
def cadastro_produto():
    codigo_p = generate_frames()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        codigo = request.form['codigo']
        conexao = conexao_bd()
        cursor = conexao.cursor()
        if generate_frames() is not None:
            cursor.execute(
            'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)', (nome, descricao, codigo_p))
        else:
            cursor.execute(
            'INSERT INTO produto (nome, descricao, codigo) VALUES (%s, %s, %s)', (nome, descricao, codigo))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))
    return render_template('cadastro_produto.html')


@app.route('/editarproduto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conexao = conexao_bd()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT  * FROM produto WHERE id = %s', (id))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        codigo = request.form['codigo']
        conexao = conexao_bd()
        pesquisa = conexao.cursor(dictionary=True)
        pesquisa.execute(
            'UPDATE produto SET nome = %s, descricao = %s, codigo = %s WHERE id = %s')
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('meu_estoque'))

    return render_template('cadastro_produto.html')


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
        numero = request.form['numero']
        tipo_produto = request.form['tipo_produto']
        valor_unitario = request.form['valor_unitario']
        valor_lote = request.form['valor_lote']
        quantidade = request.form['quantidade']
        estoque_minimo = request.form['estoque_minimo']
        data_cadastro = datetime.now().strftime('%Y-%m-%d')
        data_fabricacao = request.form['data_fabricacao']
        data_validade = request.form['data_validade']

        produto_id = request.form['produto_id']
        fornecedor_id = request.form['fornecedor_id']
        print(codigo, tipo_produto, valor_unitario, valor_lote, quantidade, estoque_minimo,
              data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id, numero)

        cursor.execute(
            'INSERT INTO lote (codigo, numero, tipo_produto, valor_unitario, valor_lote, quantidade, estoque_minimo, data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (codigo, numero, tipo_produto, valor_unitario, valor_lote, quantidade, estoque_minimo,
             data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('meu_estoque'))

    cursor.close()
    conn.close()

    return render_template('cadastro_lote.html', fornecedores=fornecedores, produtos=produtos)


@app.route('/leitorbarras')
def leitor_barras():
    return render_template('leitordebarras.html')


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
                    print("Código de Barras Identificado:", barcode_data)
                    

            # Codificar o frame em formato de imagem JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Retornar o frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Se um código de barras for identificado, pare de gerar novos quadros
            if barcode_data is not None:
                conn = conexao_bd()
                cursor = conn.cursor()
                codigo_p = barcode_data
                consulta = "SELECT * FROM produto WHERE codigo = %s"
                cursor.execute(consulta, (codigo_p,))
                resultado = cursor.fetchall()
                if len(resultado) > 0:
                    print("Produto encontrado:")

                else:
                    opcao = str(input("Deseja fazer um novo cadastro com o código de barras [S/N]? "))
                    if opcao == "S":
                        print("Vá para cadastro de produtos")
                        return barcode_data


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)