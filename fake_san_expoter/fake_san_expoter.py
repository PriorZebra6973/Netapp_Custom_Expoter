from prometheus_client import start_http_server, Gauge
import requests, time

SAN_IP = "localhost:5000"
SYSTEM_ID = "210000006D039EA000BA0C7600000FB67E5F5CC"

ENDPOINTS = {
    "volume_stats": f"storage-systems/{SYSTEM_ID}/analysed-volume-statistics",
    "drive_stats": f"storage-systems/{SYSTEM_ID}/analysed-drive-statistics",
    "controller_stats": f"storage-systems/{SYSTEM_ID}/analysed-controller-statistics",
}

gauges = {}

def get_or_create(metric, desc, labels):
    if metric not in gauges:
        gauges[metric] = Gauge(metric, desc, labels)
    return gauges[metric]

def collect():
    for name, path in ENDPOINTS.items():
        url = f"http://{SAN_IP}/devmgr/v2/{path}"
        try:
            r = requests.get(url, timeout=5)
            data = r.json()
            for obj in data:
                label = obj.get("volumeName") or obj.get("driveId") or obj.get("controllerId") or "resource"
                for k, v in obj.items():
                    if isinstance(v, (int, float)):
                        metric = f"san_{name}_{k}".lower()
                        g = get_or_create(metric, f"{name} {k}", ["id"])
                        g.labels(label).set(v)
        except Exception as e:
            print("Error fetching", url, e)

if __name__ == "__main__":
    start_http_server(9101)
    print("Exporter running on :9101/metrics")
    while True:
        collect()
        time.sleep(5)
