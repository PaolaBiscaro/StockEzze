from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
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

@app.route('/')
def index():
    connection = create_connection()
    if connection and connection.is_connected():
        return "Conexão com o banco de dados MySQL foi bem-sucedida!"
    else:
        return "Falha na conexão com o banco de dados MySQL."

if __name__ == '__main__':
    app.run(debug=True)
