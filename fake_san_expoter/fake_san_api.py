from flask import Flask, jsonify
import random

app = Flask(__name__)
SYSTEM_ID = "210000006D039EA000BA0C7600000FB67E5F5CC"

@app.route(f"/devmgr/v2/storage-systems/{SYSTEM_ID}/analysed-volume-statistics")
def volume_stats():
    return jsonify([
        {"volumeName": "vol1", "readIOps": random.randint(100,500), "writeIOps": random.randint(50,300)},
        {"volumeName": "vol2", "readIOps": random.randint(100,500), "writeIOps": random.randint(50,300)}
    ])

@app.route(f"/devmgr/v2/storage-systems/{SYSTEM_ID}/analysed-drive-statistics")
def drive_stats():
    return jsonify([
        {"driveId": "drive1", "readIOps": random.randint(100,500), "writeIOps": random.randint(50,300)}
    ])

@app.route(f"/devmgr/v2/storage-systems/{SYSTEM_ID}/analysed-controller-statistics")
def controller_stats():
    return jsonify([
        {"controllerId": "ctrlA", "cpuUsage": random.randint(10,90), "cacheHitRatio": random.uniform(80,99)}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
