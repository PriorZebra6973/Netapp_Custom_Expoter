from prometheus_client import start_http_server, Gauge
import requests, time, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SAN_IP = "10.10.10.5"
USERNAME = "admin"
PASSWORD = "Passw0rd@1234"
SYSTEM_ID = "210000006D039EA000BA0C7600000FB67E5F5CC"  # from your file

# All endpoints to fetch
ENDPOINTS = {
    "system": "storage-systems/{system_id}",
    "drives": "storage-systems/{system_id}/drives",
    "volumes": "storage-systems/{system_id}/volumes",
    "controllers": "storage-systems/{system_id}/controllers",
    "host_groups": "storage-systems/{system_id}/host-groups",
    "hosts": "storage-systems/{system_id}/hosts",
    "pools": "storage-systems/{system_id}/storage-pools",
    "drive_stats": "storage-systems/{system_id}/analysed-drive-statistics",
    "volume_stats": "storage-systems/{system_id}/analysed-volume-statistics",
    "controller_stats": "storage-systems/{system_id}/analysed-controller-statistics",
}

gauges = {}

def create_or_get_gauge(metric_name, description, label_names):
    if metric_name not in gauges:
        gauges[metric_name] = Gauge(metric_name, description, label_names)
    return gauges[metric_name]

def collect_metrics():
    for name, path in ENDPOINTS.items():
        url = f"https://{SAN_IP}/devmgr/v2/" + path.format(system_id=SYSTEM_ID)
        try:
            r = requests.get(url, verify=False, auth=(USERNAME, PASSWORD), timeout=10)
            if r.status_code != 200:
                print(f"Error {r.status_code} fetching {url}")
                continue

            data = r.json()

            # Handle both dict (single object) and list responses
            if isinstance(data, dict):
                data = [data]

            for obj in data:
                # Choose a label key
                label_key = (
                    obj.get("name") or
                    obj.get("id") or
                    obj.get("volumeName") or
                    obj.get("driveId") or
                    obj.get("controllerId") or
                    "resource"
                )
                label_key = str(label_key)

                for k, v in obj.items():
                    if isinstance(v, (int, float)):
                        metric_name = f"netapp_{name}_{k}".lower()
                        metric_name = metric_name.replace(" ", "_")
                        g = create_or_get_gauge(metric_name, f"{name} metric {k}", ["id"])
                        g.labels(label_key).set(v)

        except Exception as e:
            print(f"Exception fetching {url}: {e}")

if __name__ == "__main__":
    start_http_server(9101)
    print("Exporter running on http://localhost:9101/metrics")
    while True:
        collect_metrics()
        time.sleep(30)
