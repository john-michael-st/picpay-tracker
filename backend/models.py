from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    zona_no_momento = Column(String)
    mes = Column(Integer, default=lambda: datetime.utcnow().month)
    ano = Column(Integer, default=lambda: datetime.utcnow().year)
