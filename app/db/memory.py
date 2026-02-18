from collections import deque
from typing import Deque

LAST: dict[str, float] = {}
HISTORY: dict[str, Deque[float]] = {}
HISTORY_MAX = 200

def push_price(symbol: str, price: float):
    LAST[symbol] = price
    if symbol not in HISTORY:
        HISTORY[symbol] = deque(maxlen=HISTORY_MAX)
    HISTORY[symbol].appendleft(price)

def get_last(symbol: str) -> float | None:
    return LAST.get(symbol)

def get_history(symbol: str, n: int = 100) -> list[float]:
    if symbol not in HISTORY:
        return []
    return list(HISTORY[symbol])[:n]
