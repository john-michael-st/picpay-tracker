import os
import re
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import engine, Base, get_db
from models import Gasto
from categorizer import categorizar_gasto
from budget import calcular_resumo_mes, calcular_zona

load_dotenv()

# Cria as tabelas do banco de dados se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PicPay Tracker API")

# Habilitar CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

# Schemas Pydantic
class GastoCreate(BaseModel):
    notificacao: str
    token: Optional[str] = None

class GastoResponse(BaseModel):
    id: int
    valor: float
    descricao: str
    categoria: str
    data: datetime
    zona_no_momento: str
    mes: int
    ano: int

    class Config:
        from_attributes = True

def verificar_token(token_header: str = Header(None, alias="X-Token"), token_body: Optional[str] = None):
    if not SECRET_TOKEN:
        return # Permite rodar sem token se não estiver configurado
    
    if token_header == SECRET_TOKEN or token_body == SECRET_TOKEN:
        return True
    raise HTTPException(status_code=401, detail="Token inválido ou não fornecido")

def extrair_valor_notificacao(texto: str) -> Optional[float]:
    """
    Extrai o valor numérico de uma string (ex: 'R$ 35,90' ou 'R$ 1.000,00').
    """
    match = re.search(r'R\$\s*(\d+(?:\.\d{3})*(?:,\d{2}))', texto)
    if match:
        valor_str = match.group(1).replace('.', '').replace(',', '.')
        return float(valor_str)
    return None

@app.post("/gasto")
def criar_gasto(gasto_in: GastoCreate, x_token: str = Header(None, alias="X-Token"), db: Session = Depends(get_db)):
    verificar_token(x_token, gasto_in.token)
    
    valor = extrair_valor_notificacao(gasto_in.notificacao)
    if valor is None:
        raise HTTPException(status_code=400, detail="Não foi possível extrair o valor da notificação.")
        
    categoria = categorizar_gasto(gasto_in.notificacao)
    
    agora = datetime.utcnow()
    mes_atual = agora.month
    ano_atual = agora.year
    
    total_anterior = db.query(db.func.sum(Gasto.valor)).filter(Gasto.mes == mes_atual, Gasto.ano == ano_atual).scalar() or 0.0
    total_novo = total_anterior + valor
    zona_info = calcular_zona(total_novo)
    
    novo_gasto = Gasto(
        valor=valor,
        descricao=gasto_in.notificacao,
        categoria=categoria,
        data=agora,
        zona_no_momento=zona_info["zona"],
        mes=mes_atual,
        ano=ano_atual
    )
    
    db.add(novo_gasto)
    db.commit()
    db.refresh(novo_gasto)
    
    resumo = calcular_resumo_mes(db, mes_atual, ano_atual)
    
    return {
        "gasto": novo_gasto,
        "resumo_mes": resumo
    }

@app.get("/resumo")
def obter_resumo(db: Session = Depends(get_db)):
    agora = datetime.utcnow()
    resumo_calc = calcular_resumo_mes(db, agora.month, agora.year)
    
    ultimos = db.query(Gasto).filter(Gasto.mes == agora.month, Gasto.ano == agora.year).order_by(Gasto.data.desc()).limit(5).all()
    
    icones = {
        "Alimentação": "🍔",
        "Transporte": "🚗",
        "Saúde": "💊",
        "Lazer": "🎉",
        "Educação": "📚",
        "Moradia": "🏠"
    }
    
    categorias = []
    for cat, val in resumo_calc["gastos_por_categoria"].items():
        categorias.append({
            "nome": cat,
            "icone": icones.get(cat, "🛒"),
            "gasto": val
        })
        
    from fastapi.encoders import jsonable_encoder
    return {
        "gasto_total": resumo_calc["total_mes"],
        "teto_normal": resumo_calc["teto_normal"],
        "reserva": 200.0,
        "categorias": categorias,
        "ultimos_lancamentos": jsonable_encoder(ultimos)
    }

@app.get("/historico", response_model=List[GastoResponse])
def obter_historico(mes: Optional[int] = None, ano: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Gasto)
    if mes:
        query = query.filter(Gasto.mes == mes)
    if ano:
        query = query.filter(Gasto.ano == ano)
    
    gastos = query.order_by(Gasto.data.desc()).all()
    return gastos

@app.delete("/gasto/{id}")
def deletar_gasto(id: int, x_token: str = Header(None, alias="X-Token"), db: Session = Depends(get_db)):
    verificar_token(x_token)
    gasto = db.query(Gasto).filter(Gasto.id == id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
        
    db.delete(gasto)
    db.commit()
    return {"status": "sucesso", "mensagem": f"Gasto {id} removido."}

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
