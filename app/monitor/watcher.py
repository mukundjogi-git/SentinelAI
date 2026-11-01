import time
from app.monitor.system_monitor import get_system_metrics

CPU_LIMIT = 80
RAM_LIMIT = 85
DISK_LIMIT = 90


def check_metrics(metrics):
    alerts = []
    if metrics["cpu_percent"] > CPU_LIMIT:
        alerts.append(f"HIGH CPU: {metrics['cpu_percent']}%")
    if metrics["ram_percent"] > RAM_LIMIT:
        alerts.append(f"HIGH RAM: {metrics['ram_percent']}%")
    if metrics["disk_percent"] > DISK_LIMIT:
        alerts.append(f"HIGH DISK: {metrics['disk_percent']}%")
    return alerts


if __name__ == "__main__":
    print("SentinelAI is watching... press Ctrl + C to stop")
    while True:
        metrics = get_system_metrics()
        print(metrics)
        for alert in check_metrics(metrics):
            print("ALERT:", alert)
        time.sleep(4)