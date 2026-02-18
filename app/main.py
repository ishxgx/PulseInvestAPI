import logging
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import router
from app.core.state import stream_manager

setup_logging()
log = logging.getLogger("main")

app = FastAPI(title=settings.app_name)
app.include_router(router)

@app.on_event("startup")
async def on_startup():
    log.info("PulseInvest API started (multi-symbol on-demand).")

@app.on_event("shutdown")
async def on_shutdown():
    await stream_manager.stop_all()
    log.info("PulseInvest API stopped.")
