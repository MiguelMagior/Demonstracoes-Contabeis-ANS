DROP DATABASE IF EXISTS Despesas;
CREATE DATABASE Despesas;
USE Despesas;

CREATE TABLE Operadoras(
    cnpj CHAR(14) NOT NULL,
    registro_ans CHAR(6) NOT NULL,
    razao_social VARCHAR(225) NOT NULL,
    nome_fantasia VARCHAR(225),
    modalidade VARCHAR(50),
    ddd char(2),
    telefone CHAR(9),
    fax CHAR(11),
    email VARCHAR(100),
    logradouro VARCHAR(50),
    numero VARCHAR(10),
    complemento VARCHAR(50),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    uf CHAR(2),
    cep CHAR(8),
    representante VARCHAR(100),
    cargo_rep VARCHAR(50),
    regiao_comerc TINYINT UNSIGNED,
    data_registro DATE,
    PRIMARY KEY (cnpj),
    INDEX idx_uf_operadoras (uf)
    );

CREATE TABLE DespesasConsolidadas(
    id INT AUTO_INCREMENT,
    cnpj CHAR(14) NOT NULL,
    trimestre INT NOT NULL,
    ano YEAR NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (cnpj) REFERENCES Operadoras(cnpj)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
    INDEX idx_cnpj_despesas_consolidadas (cnpj),
    INDEX idx_periodo_despesas_consolidadas (trimestre, ano)
    );

CREATE TABLE DespesasAgregadas(
    id INT AUTO_INCREMENT,
    cnpj CHAR(14) NOT NULL,
    trimestre TINYINT NOT NULL,
    ano YEAR NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    media_valor DECIMAL(15,2) NOT NULL,
    desvio_padrao DECIMAL(15,2) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (cnpj) REFERENCES Operadoras(cnpj)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
    INDEX idx_cnpj_despesas_agregadas (cnpj),
    INDEX idx_periodo_despesas_agregadas (trimestre, ano)
    );
