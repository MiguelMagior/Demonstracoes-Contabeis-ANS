USE Despesas

LOAD DATA LOCAL INFILE 'data/operadoras.csv'
INTO TABLE Operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    registro_ans,
    cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    uf,
    cep,
    ddd,
    telefone,
    fax,
    email,
    representante,
    cargo_rep,
    regiao_comerc,
    data_registro
)
-- Limpeza básica
SET uf = UPPER(TRIM(uf)),
    cep = REPLACE(TRIM(cep), '-', ''),
    cnpj = TRIM(cnpj);


LOAD DATA LOCAL INFILE 'data/consolidado_despesas.csv'
INTO TABLE DespesasConsolidadas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    cnpj,
    @razao_social,
    trimestre,
    ano,
    valor
)
SET cnpj = TRIM(cnpj);

LOAD DATA LOCAL INFILE 'data/despesas_agregadas.csv'
INTO TABLE DespesasAgregadas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
     @uf,
     @razao_social,
     trimestre,
     ano,
     cnpj,
     @reg,
     @mod,
     valor,
     media_valor,
     desvio_padrao
)
SET cnpj = TRIM(cnpj);