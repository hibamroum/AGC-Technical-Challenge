from fastapi import FastAPI
from src.api.v1 import router as v1_router

app = FastAPI(title="Women Public Safety Chat", version="1.0.0")
app.include_router(v1_router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
