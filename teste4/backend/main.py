from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
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
def list_companies(
        page: int = Query(1, ge=1, description="Número da página"),
        limit: int = Query(10, ge=1, le=100, description="Itens por página"),
        search: str | None = Query(None, description="Procurar por CNPK/Razao Social"),
        db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * limit

        query = db.query(
            Operadora.cnpj,
            Operadora.razao_social
        )
        total = query.count()

        if search:
            query = query.filter(
                or_(
                    Operadora.razao_social.like(f"%{search}%"),
                    Operadora.cnpj.like(f"%{search}%")
                )
            )

        companies = query \
            .order_by(Operadora.razao_social) \
            .offset(offset) \
            .limit(limit) \
            .all()

        result = [
            {
                "razao_social": op.razao_social,
                "cnpj": op.cnpj,
            }
            for op in companies
        ]

        return {
            "data": result,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route 2: search company by CNPJ
@app.get("/api/operadoras/{cnpj}")
def search_company(
        cnpj: str,
        db: Session = Depends(get_db)):
    try:
        company = (db.query(Operadora)
                     .filter(Operadora.cnpj == cnpj)
                     .first())
        if not company:
            raise HTTPException(status_code=404, detail="Operadora não encontrada")

        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route 3: company expenses
@app.get("/api/operadoras/{cnpj}/despesas")
def list_expenses_from_company(
        cnpj: str,
        db: Session = Depends(get_db)
):
    try:
        company = db.query(Operadora).filter(Operadora.cnpj == cnpj).first()
        if not company:
            raise HTTPException(status_code=404, detail="Operadora não encontrada")

        expenses = (db.query(DespesaConsolidada)
                    .filter(DespesaConsolidada.cnpj == cnpj)
                    .all())

        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route 4: statistics
@app.get("/api/estatisticas")
def list_statistics(db: Session = Depends(get_db)):
    try:
        stats = db.query(
            func.sum(DespesaAgregada.valor).label("general_sum"),
            func.round(func.avg(DespesaAgregada.valor), 2).label("general_average"),
        ).one()

        top5 = (db.query(
            DespesaAgregada.cnpj,
            Operadora.razao_social,
            Operadora.uf,
            func.sum(DespesaAgregada.valor).label("total_op"),
            func.round(func.avg(DespesaAgregada.valor), 2).label("average_op")
        ).join(
            Operadora, DespesaAgregada.cnpj == Operadora.cnpj
        ).group_by(DespesaAgregada.cnpj)
                .order_by(desc("total_op"))
                .limit(5)
                .all())

        expenses_by_uf = (
            db.query(
                Operadora.uf,
                func.sum(DespesaAgregada.valor).label("total")
            )
            .join(Operadora, Operadora.cnpj == DespesaAgregada.cnpj)
            .group_by(Operadora.uf)
            .all()
        )

        return {
            "soma_geral": stats.general_sum,
            "media_geral": stats.general_average,
            "despesas_por_uf": [
                {
                    "uf": item.uf,
                    "total": float(item.total)
                }
                for item in expenses_by_uf
            ],

            "top_5_operadoras": [
                {
                    "cnpj": item.cnpj,
                    "razao_social": item.razao_social,
                    "uf": item.uf,
                    "total_despesas": item.total_op,
                    "media_valor_despesa": item.average_op,
                }
                for item in top5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
