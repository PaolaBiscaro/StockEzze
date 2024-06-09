import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "paola05052015",
    "database": "stockezze_oficial"
}

# Função para conectar ao banco de dados
def conectar_bd():
    return mysql.connector.connect(**db_config)

# Função para capturar imagem da câmera e detectar código de barras
def capture_and_detect():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Código para detectar código de barras

    cap.release()
    # Retorna o código de barras detectado ou uma mensagem de erro
    return "Código de barras detectado"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan_barcode", methods=["GET"])
def scan_barcode():
    barcode_data = capture_and_detect()
    return jsonify({"produto": {"codigo": barcode_data, "nome": "Produto 1", "descricao": "Descrição do Produto 1"}})

@app.route("/confirm_barcode", methods=["POST"])
def confirm_barcode():
    barcode_data = request.form["barcode_data"]
    return jsonify({"produto": {"codigo": barcode_data, "nome": "Produto 2", "descricao": "Descrição do Produto 2"}})

if __name__ == "__main__":
    app.run(debug=True)
