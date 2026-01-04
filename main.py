# from typing import Union
from fastapi import FastAPI
from api.app.health import router as health_router
from api.app.run import router as run_router

app = FastAPI(title="Run club api")

app.include_router(health_router)
app.include_router(run_router)
