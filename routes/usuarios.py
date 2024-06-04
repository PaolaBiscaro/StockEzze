from flask import Flask, Blueprint, render_template
from mysql.connector import connect

#helo
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import mysql.connector

#helo

app = dash.Dash(__name__)
app = Flask(__name__)

# Função para criar a conexão com o banco de dados
def conexao_db():
    return connect(
        host='127.0.0.1',
        database='stockezze_oficial',
        user='root',
        password='Helo761.'
    )

usuario = Blueprint('usuario', __name__)

@usuario.route('/meuestoque')
def meu_estoque():
    conn = conexao_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Produto')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('estoqueprincipal.html', produtos=produtos)



@usuario.route('/leitorbarras')
def leitor_barras():
    return render_template("leitordebarras.html")

@usuario.route('/cadastroproduto')
def cadastro_produtos():
    return render_template("cadastrodeprodutos.html")


@usuario.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


# @usuario.route('/relatorios')
# def relatorios():
    


#     # Query para obter dados anuais e mensais de faturamento
#     query_faturamento_anual = '''
#     SELECT YEAR(data) as Ano, SUM(quantidade * valor_unitario) as Faturamento_Anual, SUM(quantidade) as Produtos_Vendidos
#     FROM EntradaSaida es
#     JOIN Lote l ON es.lote_id = l.id
#     WHERE tipo = 'saida'
#     GROUP BY YEAR(data)
#     ORDER BY Ano
#     '''

#     query_faturamento_mensal = '''
#     SELECT YEAR(data) as Ano, MONTH(data) as Mes, SUM(quantidade * valor_unitario) as Faturamento_Mensal
#     FROM EntradaSaida es
#     JOIN Lote l ON es.lote_id = l.id
#     WHERE tipo = 'saida'
#     GROUP BY YEAR(data), MONTH(data)
#     ORDER BY Ano, Mes
#     '''

#     df_anual = pd.read_sql(query_faturamento_anual,conexao_db)
#     df_mensal = pd.read_sql(query_faturamento_mensal, conexao_db)

#     # Cálculo do faturamento total
#     faturamento_total = df_anual['Faturamento_Anual'].sum()
#     produtos_vendidos_total = df_anual['Produtos_Vendidos'].sum()



#     # Inicializando o app Dash


#     # Layout do dashboard
#     app.layout = html.Div(children=[
#         html.H1(children='Dashboard de Faturamento'),

#         html.Div(children=[
#             html.Div(children=[
#                 html.H3(children='Faturamento Total'),
#                 html.P(children=f'R$ {faturamento_total:,.2f}')
#             ], style={'padding': 10, 'flex': 1}),

#             html.Div(children=[
#                 html.H3(children='Produtos Vendidos'),
#                 html.P(children=f'{produtos_vendidos_total}')
#             ], style={'padding': 10, 'flex': 1}),
#         ], style={'display': 'flex'}),

#         dcc.Graph(
#             id='faturamento-anual',
#             figure={
#                 'data': [
#                     go.Bar(
#                         x=df_anual['Ano'],
#                         y=df_anual['Faturamento_Anual'],
#                         name='Faturamento Anual'
#                     )
#                 ],
#                 'layout': go.Layout(
#                     title='Faturamento Anual',
#                     xaxis={'title': 'Ano'},
#                     yaxis={'title': 'Faturamento (R$)'}
#                 )
#             }
#         ),

#         dcc.Graph(
#             id='faturamento-mensal',
#             figure={
#                 'data': [
#                     go.Scatter(
#                         x=df_mensal[df_mensal['Ano'] == ano]['Mes'],
#                         y=df_mensal[df_mensal['Ano'] == ano]['Faturamento_Mensal'],
#                         mode='lines+markers',
#                         name=str(ano)
#                     ) for ano in df_mensal['Ano'].unique()
#                 ],
#                 'layout': go.Layout(
#                     title='Faturamento Mensal',
#                     xaxis={'title': 'Mês'},
#                     yaxis={'title': 'Faturamento (R$)'}
#                 )
#             }
#         )
#     ])

#     return render_template('relatorio.html')

# # Executar o app
# app.run_server(debug=True)


# Quando puder testa
