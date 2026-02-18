import asyncio
import logging
from typing import Dict

from app.services.market_stream import stream_trades

log = logging.getLogger("stream_manager")


class StreamManager:
    def __init__(self):
        self._stop_events: Dict[str, asyncio.Event] = {}
        self._tasks: Dict[str, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def ensure_running(self, symbol: str) -> bool:
        """
        Asegura que el stream de `symbol` está activo.
        Devuelve True si lo acaba de arrancar, False si ya estaba corriendo.
        """
        sym = symbol.strip().lower()

        async with self._lock:
            # Si ya hay tarea viva, no hacemos nada
            task = self._tasks.get(sym)
            if task and not task.done():
                return False

            stop_event = asyncio.Event()
            self._stop_events[sym] = stop_event

            log.info(f"Starting stream for {sym}")
            self._tasks[sym] = asyncio.create_task(stream_trades(sym, stop_event))
            return True

    async def stop(self, symbol: str) -> bool:
        sym = symbol.strip().lower()
        async with self._lock:
            stop_event = self._stop_events.get(sym)
            task = self._tasks.get(sym)
            if not stop_event or not task:
                return False
            stop_event.set()
            task.cancel()
            return True

    async def stop_all(self):
        async with self._lock:
            for sym, ev in self._stop_events.items():
                ev.set()
            for sym, task in self._tasks.items():
                task.cancel()
            self._stop_events.clear()
            self._tasks.clear()

    def active_symbols(self) -> list[str]:
        return [sym for sym, task in self._tasks.items() if task and not task.done()]
