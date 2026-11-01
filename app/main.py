from fastapi import FastAPI
from app.monitor.system_monitor import get_system_metrics

app = FastAPI(title="SentinelAI")


@app.get("/")
def home():
    return {"message": "SentinelAI is running"}


@app.get("/metrics")
def metrics():
    return get_system_metrics()