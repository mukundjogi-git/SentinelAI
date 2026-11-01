from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, SessionLocal
from app.monitor.system_monitor import get_system_metrics
from app.monitor.watcher import check_metrics, CPU_LIMIT, RAM_LIMIT, DISK_LIMIT

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelAI")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def incident_to_dict(incident):
    return {
        "id": incident.id,
        "title": incident.title,
        "metric": incident.metric,
        "value": incident.value,
        "severity": incident.severity,
        "status": incident.status,
        "created_at": incident.created_at,
    }


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


@app.post("/incidents/detect")
def detect_incidents(db: Session = Depends(get_db)):
    current = get_system_metrics()
    checks = [
        ("cpu", current["cpu_percent"], CPU_LIMIT),
        ("ram", current["ram_percent"], RAM_LIMIT),
        ("disk", current["disk_percent"], DISK_LIMIT),
    ]
    created = []
    for name, value, limit in checks:
        if value <= limit:
            continue
        already_open = (
            db.query(models.Incident)
            .filter(models.Incident.metric == name, models.Incident.status == "open")
            .first()
        )
        if already_open:
            continue
        incident = models.Incident(
            title=f"High {name.upper()} usage",
            metric=name,
            value=value,
            severity="high" if value > 95 else "medium",
        )
        db.add(incident)
        created.append(incident)
    db.commit()
    for incident in created:
        db.refresh(incident)
    return {"created": len(created), "incidents": [incident_to_dict(i) for i in created]}


@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).order_by(models.Incident.id.desc()).all()
    return [incident_to_dict(i) for i in incidents]