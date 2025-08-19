from prometheus_client import start_http_server, Gauge
import requests, time, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authentication & cluster list
USERNAME = "admin"
PASSWORD = "netapp123"
CLUSTERS = ["10.10.10.100", "10.10.10.101", "10.10.10.102", "10.10.10.103", "10.10.10.104"]

# Define Prometheus Gauges
cluster_latency_total = Gauge("netapp_cluster_latency_ms", "Cluster latency (ms)", ["cluster"])
cluster_iops_total = Gauge("netapp_cluster_iops", "Cluster total IOPS", ["cluster"])
volume_iops = Gauge("netapp_volume_iops", "Volume IOPS", ["cluster", "volume"])
aggregate_count = Gauge("netapp_aggregate_count", "Total aggregates", ["cluster"])
svm_count = Gauge("netapp_svm_count", "Total SVMs", ["cluster"])
lun_count = Gauge("netapp_lun_count", "Total LUNs", ["cluster"])

def fetch_json(cluster_ip, path):
    url = f"https://{cluster_ip}/api{path}"
    try:
        r = requests.get(url, auth=(USERNAME, PASSWORD), verify=False, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[ERROR] Cluster {cluster_ip} path {path}: {e}")
    return {}

def collect_metrics():
    for cluster in CLUSTERS:
        # Cluster stats
        cluster_data = fetch_json(cluster, "/cluster")
        if "metric" in cluster_data:
            cluster_latency_total.labels(cluster).set(cluster_data["metric"]["latency"]["total"])
            cluster_iops_total.labels(cluster).set(cluster_data["metric"]["iops"]["total"])

        # Volumes
        vol_data = fetch_json(cluster, "/storage/volumes")
        if "records" in vol_data:
            for vol in vol_data["records"]:
                volume_iops.labels(cluster, vol["name"]).set(
                    vol.get("statistics", {}).get("iops", {}).get("total", 0)
                )

        # Aggregates
        agg_data = fetch_json(cluster, "/storage/aggregates")
        if "records" in agg_data:
            aggregate_count.labels(cluster).set(len(agg_data["records"]))

        # SVMs
        svm_data = fetch_json(cluster, "/svm/svms")
        if "records" in svm_data:
            svm_count.labels(cluster).set(len(svm_data["records"]))

        # LUNs
        lun_data = fetch_json(cluster, "/storage/luns")
        if "records" in lun_data:
            lun_count.labels(cluster).set(len(lun_data["records"]))

if __name__ == "__main__":
    start_http_server(9101)  # Exporter on port 9101
    print("🚀 NetApp Exporter running on port 9101")
    while True:
        collect_metrics()
        time.sleep(30)
