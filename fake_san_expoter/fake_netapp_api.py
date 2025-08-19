from flask import Flask, jsonify
import random, time

app = Flask(__name__)

@app.route("/api/cluster", methods=["GET"])
def cluster_info():
    # Simulate cluster-level metrics
    return jsonify({
        "version": {"full": "9.15.1"},
        "name": "fake-cluster",
        "uuid": "1234-5678-90",
        "metric": {
            "latency": {
                "read": random.randint(0, 2),
                "write": random.randint(0, 2),
                "total": random.randint(0, 150)
            },
            "iops": {
                "read": random.randint(0, 5000),
                "write": random.randint(0, 5000),
                "total": random.randint(0, 10000)
            },
            "throughput": {
                "read": random.randint(10**6, 10**7),
                "write": random.randint(10**6, 10**7),
                "total": random.randint(10**7, 10**8)
            }
        }
    })

@app.route("/api/storage/volumes", methods=["GET"])
def volumes():
    # Simulate per-volume statistics
    vols = []
    for i in range(1, 4):  # fake 3 volumes
        vols.append({
            "uuid": f"vol-{i}",
            "name": f"volume_{i}",
            "statistics": {
                "iops": {
                    "read": random.randint(0, 1000),
                    "write": random.randint(0, 1000),
                    "total": random.randint(0, 2000),
                },
                "latency": {
                    "read": random.random(),
                    "write": random.random(),
                    "total": random.uniform(0.5, 2.0),
                },
                "throughput": {
                    "read": random.randint(10**5, 10**6),
                    "write": random.randint(10**5, 10**6),
                    "total": random.randint(10**6, 10**7),
                }
            }
        })
    return jsonify({"records": vols})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
