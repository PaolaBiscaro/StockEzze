#Banco de Dados

create database stockezze_oficial;
use stockezze_oficial;

CREATE TABLE Produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    codigo VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Fornecedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    marca VARCHAR(255),
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    rua VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255),
    estado VARCHAR(2),
    cep VARCHAR(10),
    email VARCHAR(255),
    telefone VARCHAR(15)
);

CREATE TABLE Lote (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    numero VARCHAR(50) NOT NULL,
    tipo_produto VARCHAR(255),
    valor_unitario DECIMAL(10, 2),
    valor_lote DECIMAL(10, 2),
    quantidade INT,
    estoque_minimo INT,
    data_cadastro DATE,
    data_fabricacao DATE,
    data_validade DATE,
    produto_id INT,
    fornecedor_id INT,
    FOREIGN KEY (produto_id) REFERENCES Produto(id),
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(id)
);

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
    -- Outros campos conforme necessário
);


CREATE TABLE EntradaSaida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('entrada', 'saida') NOT NULL,
    data DATE NOT NULL,
    quantidade INT NOT NULL,
    produto_id INT,
    lote_id INT,
    usuario_id INT,
    FOREIGN KEY (produto_id) REFERENCES Produto(id),
    FOREIGN KEY (lote_id) REFERENCES Lote(id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);