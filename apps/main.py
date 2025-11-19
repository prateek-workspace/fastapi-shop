# apps/main.py
import logging
from fastapi import FastAPI

from config.routers import RouterManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi_app")

app = FastAPI(title="FastAPI Shop", version="0.1.0")


@app.on_event("startup")
def startup_event():
    # Load routers dynamically
    RouterManager(app).import_routers()
    logger.info("Routers loaded successfully.")


@app.get("/")
def health():
    return {"status": "ok"}
