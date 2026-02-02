from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import get_db
from models import Operadora, DespesaConsolidada, DespesaAgregada

app = FastAPI(
    title="API Demonstrações Contábeis ANS",
    description="API para consulta de operadoras de saúde disponibilizados pela Agência Nacional de Saúde Suplementar",
    version="1.0.0"
)

# Test Route
@app.get("/")
def home():
    return {"message": "A API está funcionando"}

# Route 1: list all companies (pagination)
@app.get("/api/operadoras")
def list_operadoras(
        page: int = Query(1, ge=1, description="Número da página"),
        limit: int = Query(10, ge=1, le=100, description="Itens por página"),
        db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    query = db.query(
        Operadora.cnpj,
        Operadora.razao_social
    )
    total = query.count()

    operadoras = query \
        .order_by(Operadora.razao_social) \
        .offset(offset) \
        .limit(limit) \
        .all()

    result = [
        {
            "razao_social": op.razao_social,
            "cnpj": op.cnpj,
        }
        for op in operadoras
    ]

    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }


# Route 2: search company by CNPJ
@app.get("/api/operadoras/{cnpj}")
def search_operadora(
        cnpj: str,
        db: Session = Depends(get_db)):
    operadora = (db.query(Operadora)
                .filter(Operadora.cnpj == cnpj)
                .first())
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    return operadora


# Route 3: company expenses
@app.get("/api/operadoras/{cnpj}/despesas")
def lits_despesas_operadora(
        cnpj: str,
        db: Session = Depends(get_db)
):
    operadora = db.query(Operadora).filter(Operadora.cnpj == cnpj).first()
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    despesas = (db.query(DespesaConsolidada)
                .filter(DespesaConsolidada.cnpj == cnpj)
                .all())

    total = db.query(DespesaConsolidada).filter(DespesaConsolidada.cnpj == cnpj).count()

    return {
        "operadora": operadora.razao_social,
        "despesas": despesas,
        "total": total,
    }


# Route 4: statistics
@app.get("/api/estatisticas")
def list_statistics(db: Session = Depends(get_db)):
    try:
        stats = db.query(
            func.sum(DespesaAgregada.valor).label("soma_total"),
            func.round(func.avg(DespesaAgregada.valor),2).label("media_geral"),
        )

        top5 = (db.query(
            DespesaAgregada.cnpj,
            Operadora.razao_social,
            func.sum(DespesaAgregada.valor).label("valor_total"),
            func.round(func.avg(DespesaAgregada.valor),2).label("media")
        ).join(
            Operadora, DespesaAgregada.cnpj == Operadora.cnpj
        ).group_by(DespesaAgregada.cnpj)
        .order_by(desc("valor_total"))
        .limit(5)
        .all())

        soma_total = stats[0].soma_total
        media_geral = stats[0].media_geral

        return {
            "soma_total": soma_total,
            "media_geral": media_geral,
            "top_5_operadoras": [
                {
                    "cnpj": item.cnpj,
                    "razao_social": item.razao_social,
                    "total_despesas": item.valor_total,
                    "media_valor_despesa": item.media,
                }
                for item in top5 ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
