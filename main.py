from prometheus_client import start_http_server, Gauge
import psutil
import time
import os

EXPORTER_HOST = os.getenv("EXPORTER_HOST", "localhost")
EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", 8000))

cpu_core_usage = Gauge('cpu_usage', 'CPU usage percentage per core', ['core'])
memory = Gauge('memory_usage', 'Memory metrics in megabytes', ['type'])
disk = Gauge('disk_usage', 'Disk space metrics in gigabytes', ['type'])


def collect_metrics():
    core_percentages = psutil.cpu_percent(percpu=True)
    for core, usage in enumerate(core_percentages):
        cpu_core_usage.labels(core=str(core)).set(usage)

    mem = psutil.virtual_memory()
    memory.labels(type="total").set(mem.total / (1024 * 1024))
    memory.labels(type="used").set(mem.used / (1024 * 1024))

    disk_usage = psutil.disk_usage('/')
    disk.labels(type="total").set(disk_usage.total / (1024 * 1024 * 1024))
    disk.labels(type="used").set(disk_usage.used / (1024 * 1024 * 1024))


if __name__ == "__main__":
    print(f"Starting exporter on {EXPORTER_HOST}:{EXPORTER_PORT}")
    start_http_server(EXPORTER_PORT, addr=EXPORTER_HOST)
    print(f"Exporter running on http://{EXPORTER_HOST}:{EXPORTER_PORT}")

    while True:
        collect_metrics()
        time.sleep(5)
