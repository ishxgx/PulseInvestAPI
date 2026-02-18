import math
from app.db.memory import get_last, get_history

def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)

def _std(xs: list[float]) -> float:
    m = _mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)

def _decide_action(trend: str, score: float, volatility: float) -> tuple[str, str]:
    """
    Reglas MUY simples:
    - Si hay volatilidad alta => WAIT (evitar ruido)
    - Si tendencia up y score suficiente => BUY
    - Si tendencia down y score suficiente => SELL
    - Si score bajo => WAIT
    """
    # Ajusta estos umbrales a tu gusto
    VOL_HIGH = 2.0        # si el std de precios es alto, es más "ruidoso"
    SCORE_STRONG = 2.0    # fuerza de tendencia (según tu escala actual)
    SCORE_WEAK = 0.8

    if volatility >= VOL_HIGH:
        return ("WAIT", "Volatilidad alta: mejor esperar confirmación.")

    if score < SCORE_WEAK:
        return ("WAIT", "Señal débil: no hay una ventaja clara.")

    if trend == "up" and score >= SCORE_STRONG:
        return ("BUY", "Tendencia alcista con fuerza suficiente.")

    if trend == "down" and score >= SCORE_STRONG:
        return ("SELL", "Tendencia bajista con fuerza suficiente.")

    return ("WAIT", "Condiciones mixtas: esperar un mejor momento.")

async def compute_signals(symbol: str) -> dict:
    sym = symbol.strip().lower()
    last = get_last(sym)

    if last is None:
        return {"symbol": sym, "status": "warming_up", "message": "Esperando datos..."}

    prices = get_history(sym, 100)

    if len(prices) < 20:
        return {
            "symbol": sym,
            "status": "warming_up",
            "last_price": float(last),
            "message": "Aún no hay suficientes datos (mínimo 20).",
        }

    recent = prices[:20]
    older = prices[20:40] if len(prices) >= 40 else prices[-20:]

    ma_recent = _mean(recent)
    ma_older = _mean(older)

    trend = "up" if ma_recent > ma_older else "down"
    vol = _std(prices[:50]) if len(prices) >= 50 else _std(prices)

    diff = abs(ma_recent - ma_older) / ma_older
    score = max(0.0, min(100.0, diff * 1000))  # escala simple

    action, reason = _decide_action(trend, score, vol)

    return {
        "symbol": sym,
        "status": "ok",
        "last_price": float(last),
        "trend": trend,
        "ma_recent": ma_recent,
        "ma_older": ma_older,
        "volatility": vol,
        "score": score,
        "action": action,     # BUY / SELL / WAIT
        "reason": reason,     # explicación corta
        "note": "MVP educativo. No es consejo financiero.",
    }
