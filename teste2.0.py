import pandas as pd
import mysql.connector
from flask import Flask
from dash import Dash, dcc, html
import plotly.express as px

# Configuração do Flask
server = Flask(__name__)

# Conexão com o banco de dados MySQL
def conexao_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        database='stockezze_oficial',
        user='root',
        password='paola05052015'
    )

# Obter dados do banco de dados
def obter_dados():
    conn = conexao_db()
    
    query_faturamento_anual = '''
    SELECT CAST(YEAR(es.data) AS UNSIGNED) as Ano, SUM(es.quantidade * l.valor_unitario) as Faturamento_Anual
    FROM EntradaSaida es
    JOIN Lote l ON es.lote_id = l.id
    WHERE es.tipo = 'saida'
    GROUP BY Ano
    ORDER BY Ano
    '''
    
    query_faturamento_mensal = '''
    SELECT CAST(YEAR(es.data) AS UNSIGNED) as Ano, MONTH(es.data) as Mes, SUM(es.quantidade * l.valor_unitario) as Faturamento_Mensal
    FROM EntradaSaida es
    JOIN Lote l ON es.lote_id = l.id
    WHERE es.tipo = 'saida'
    GROUP BY Ano, Mes
    ORDER BY Ano, Mes
    '''
    
    query_total_produtos = 'SELECT COUNT(*) as Total_Produtos FROM Produto'
    
    query_total_faturamento = '''
    SELECT SUM(es.quantidade * l.valor_unitario) as Faturamento_Total
    FROM EntradaSaida es
    JOIN Lote l ON es.lote_id = l.id
    WHERE es.tipo = 'saida'
    '''
    
    df_anual = pd.read_sql(query_faturamento_anual, conn)
    df_mensal = pd.read_sql(query_faturamento_mensal, conn)
    df_total_produtos = pd.read_sql(query_total_produtos, conn)
    df_total_faturamento = pd.read_sql(query_total_faturamento, conn)

    conn.close()
    
    return df_anual, df_mensal, df_total_produtos.iloc[0]['Total_Produtos'], df_total_faturamento.iloc[0]['Faturamento_Total']

# Configuração do Dash
app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Obter os dados
df_anual, df_mensal, total_produtos, total_faturamento = obter_dados()

# Gráfico de Faturamento Anual
fig_anual = px.bar(df_anual, x='Ano', y='Faturamento_Anual', title='Faturamento Anual')

# Gráfico de Faturamento Mensal
fig_mensal = px.bar(df_mensal, x='Mes', y='Faturamento_Mensal', color='Ano', title='Faturamento Mensal', barmode='group')

# Layout do Dash
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Faturamento'),

    html.Div(children=[
        html.Div(children=f'Total de Produtos: {total_produtos}',
        style={
            'padding': 40,
            'fontSize': 25,
            'border': '2px solid black',  # Adiciona uma borda preta de 2px
            'borderRadius': 5,  # Borda arredondada
        }),
        html.Div(children=f'Faturamento Total: R$ {total_faturamento:,.2f}', style={
            'padding': 40,
            'fontSize': 25,
            'border': '2px solid black',  # Adiciona uma borda preta de 2px
            'borderRadius': 5,  # Borda arredondada
        }),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    dcc.Graph(
        id='faturamento-anual',
        figure=fig_anual
    ),

    dcc.Graph(
        id='faturamento-mensal',
        figure=fig_mensal
    )
])

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
