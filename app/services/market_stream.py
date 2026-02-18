import asyncio
import json
import logging

import websockets
from app.db.memory import push_price

log = logging.getLogger("market_stream")
BINANCE_WS_BASE = "wss://stream.binance.com:9443/ws"

def normalize_symbol(symbol: str) -> str:
    return symbol.strip().lower()

async def stream_trades(symbol: str, stop_event: asyncio.Event):
    sym = normalize_symbol(symbol)
    url = f"{BINANCE_WS_BASE}/{sym}@trade"

    while not stop_event.is_set():
        try:
            log.info(f"Connecting to {url}")
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                while not stop_event.is_set():
                    msg = await ws.recv()
                    data = json.loads(msg)
                    price = float(data["p"])
                    push_price(sym, price)
        except Exception as e:
            log.warning(f"WS error ({sym}): {e}. Reconnecting in 2s...")
            await asyncio.sleep(2)
