from sqlalchemy import func
from models import Gasto

TETO_NORMAL = 300.0
TETO_EMERGENCIAL = 500.0

def calcular_zona(total_gasto: float) -> dict:
    """
    Calcula a zona de alerta, percentuais, valores restantes e a mensagem de alerta.
    Zonas:
      - Verde: R$ 0 a R$ 250
      - Amarela: R$ 251 a R$ 300 (alerta: 'Próximo do teto')
      - Laranja: R$ 301 a R$ 500 (alerta: 'Teto atingido — consumindo reserva emergencial')
      - Vermelha: acima de R$ 500 (alerta crítico)
    """
    percentual_normal = min((total_gasto / TETO_NORMAL) * 100, 100.0) if TETO_NORMAL > 0 else 100.0
    restante_normal = max(TETO_NORMAL - total_gasto, 0.0)
    
    if total_gasto <= 250:
        zona = "verde"
        mensagem = "Dentro do orçamento normal."
        percentual_emergencial = 0.0
        restante_emergencial = 200.0
    elif total_gasto <= 300:
        zona = "amarela"
        mensagem = "Próximo do teto normal."
        percentual_emergencial = 0.0
        restante_emergencial = 200.0
    elif total_gasto <= 500:
        zona = "laranja"
        mensagem = "Teto atingido — consumindo reserva emergencial."
        gasto_emergencial = total_gasto - TETO_NORMAL
        percentual_emergencial = min((gasto_emergencial / 200.0) * 100, 100.0)
        restante_emergencial = max(200.0 - gasto_emergencial, 0.0)
    else:
        zona = "vermelha"
        mensagem = "Alerta Crítico: Limites excedidos!"
        percentual_emergencial = 100.0
        restante_emergencial = 0.0

    return {
        "zona": zona,
        "percentual_normal": round(percentual_normal, 2),
        "percentual_emergencial": round(percentual_emergencial, 2),
        "restante_normal": round(restante_normal, 2),
        "restante_emergencial": round(restante_emergencial, 2),
        "mensagem_alerta": mensagem
    }

def calcular_resumo_mes(db_session, mes: int, ano: int) -> dict:
    """
    Consulta os gastos de um mês específico e retorna o resumo com base no orçamento.
    """
    total = db_session.query(func.sum(Gasto.valor)).filter(Gasto.mes == mes, Gasto.ano == ano).scalar() or 0.0
    
    gastos = db_session.query(Gasto.categoria, func.sum(Gasto.valor)).filter(Gasto.mes == mes, Gasto.ano == ano).group_by(Gasto.categoria).all()
    gastos_por_categoria = {cat: val for cat, val in gastos}

    zona_info = calcular_zona(total)
    
    return {
        "total_mes": round(total, 2),
        "teto_normal": TETO_NORMAL,
        "teto_emergencial": TETO_EMERGENCIAL,
        "gastos_por_categoria": gastos_por_categoria,
        **zona_info
    }
