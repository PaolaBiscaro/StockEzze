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

CREATE TABLE lote (
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
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
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



INSERT INTO produto (id, nome, descricao, codigo, fornecedor_id)
VALUES ('03', 'Produto 03', 'Exemplo de um produto 03, para testes', '373737', '1');

INSERT INTO fornecedor (
    nome, marca, cnpj, rua, bairro, cidade, estado, cep, email, telefone) 
VALUES ('Fornecedor 01',  'Marca Produto 01', '12.345.678/0001-99', 'Rua Teste','Bairro Teste','Cidade Teste','SP','12345-678', 'teste@fornecedor.com','(11) 1234-5678');

INSERT INTO Lote (codigo, numero, tipo_produto, valor_unitario, valor_lote, quantidade, estoque_minimo, data_cadastro, data_fabricacao, data_validade, produto_id, fornecedor_id) 
VALUES ('COD12345', 'NUM98765', 'Produto Exemplo', 10.50, 1050.00, 100, 10, '2024-06-05','2022-05-20', '2025-05-20', 3, 1 
);


INSERT INTO Lote (
    codigo,
    numero,
    tipo_produto,
    valor_unitario,
    valor_lote,
    quantidade,
    estoque_minimo,
    data_cadastro,
    data_fabricacao,
    data_validade,
    produto_id,
    fornecedor_id

) VALUES (
    'COD12345',        -- codigo
    'NUM98765',        -- numero
    'Produto Exemplo', -- tipo_produto
    10.50,             -- valor_unitario
    1050.00,           -- valor_lote
    100,               -- quantidade
    10,                -- estoque_minimo
    '2024-06-05',      -- data_cadastro
    '2024-05-20',      -- data_fabricacao
    '2025-05-20',      -- data_validade
    1,                 -- produto_id (deve corresponder a um ID válido na tabela Produto)
    1                  -- fornecedor_id (deve corresponder a um ID válido na tabela Fornecedor)
);

INSERT INTO Fornecedor (
    nome, marca, cnpj, rua, bairro, cidade, estado, cep, email, telefone
) VALUES (
    'Fornecedor Exemplo',    -- nome
    'Marca Exemplo',         -- marca
    '12.345.678/0001-99',    -- cnpj
    'Rua Exemplo',           -- rua
    'Bairro Exemplo',        -- bairro
    'Cidade Exemplo',        -- cidade
    'EX',                    -- estado
    '12345-678',             -- cep
    'exemplo@fornecedor.com',-- email
    '(11) 1234-5678'         -- telefone
);

