import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.signals import compute_signals
from app.db.memory import get_last
from app.core.state import stream_manager

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/symbols/active")
async def active_symbols():
    return {"active": stream_manager.active_symbols()}

@router.get("/signals")
async def signals(symbol: str = "btcusdt"):
    # auto-arranca stream si no estaba corriendo
    await stream_manager.ensure_running(symbol)
    return await compute_signals(symbol)

@router.websocket("/ws/prices/{symbol}")
async def ws_prices(ws: WebSocket, symbol: str):
    await ws.accept()
    sym = symbol.strip().lower()

    # auto-arranca stream si no estaba corriendo
    await stream_manager.ensure_running(sym)

    try:
        while True:
            last = get_last(sym)
            if last is None:
                await ws.send_json({"symbol": sym, "status": "warming_up"})
            else:
                await ws.send_json({"symbol": sym, "price": float(last)})
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        return
