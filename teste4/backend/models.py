from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Operadora(Base):
    __tablename__ = "Operadoras"

    cnpj = Column(String(14), primary_key=True, index=True)
    registro_ans = Column(String(6))
    razao_social = Column(String(255))
    nome_fantasia = Column(String(255))
    modalidade = Column(String(50))
    ddd = Column(String(2))
    telefone = Column(String(9))
    fax = Column(String(9))
    email = Column(String(100))
    logradouro = Column(String(50))
    numero = Column(String(10))
    complemento = Column(String(50))
    bairro = Column(String(50))
    cidade = Column(String(50))
    uf = Column(String(2))
    cep = Column(String(8))
    representante = Column(String(100))
    cargo_rep = Column(String(50))
    regiao_comerc = Column(Integer)
    data_registro = Column(Date)


class DespesaConsolidada(Base):
    __tablename__ = "DespesasConsolidadas"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(14), index=True)
    trimestre = Column(Integer)
    ano = Column(Date)
    valor = Column(DECIMAL(15, 2))

class DespesaAgregada(Base):
    __tablename__ = "DespesasAgregadas"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(14), index=True)
    trimestre = Column(Integer)
    ano = Column(Date)
    valor = Column(DECIMAL(15, 2))
    media_valor = Column(DECIMAL(15, 2))
    desvio_padrao = Column(DECIMAL(15, 2))