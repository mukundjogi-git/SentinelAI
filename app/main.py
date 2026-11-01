from fastapi import FastAPI
from app.monitor.system_monitor import get_system_metrics
from app.monitor.watcher import check_metrics

app = FastAPI(title="SentinelAI")


@app.get("/")
def home():
    return {"message": "SentinelAI is running"}


@app.get("/metrics")
def metrics():
    return get_system_metrics()


@app.get("/alerts")
def alerts():
    current = get_system_metrics()
    problems = check_metrics(current)
    return {
        "status": "ALERT" if problems else "HEALTHY",
        "alert_count": len(problems),
        "alerts": problems,
        "metrics": current,
    }