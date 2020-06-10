import requests
import time
import json
import os

SERVICES = ["python-executor", "admin-service", "kind", "ui", "workflow-engine"]


def init_status():
    if not os.path.exists(".runtime"):
        os.mkdir(".runtime")
    if not os.path.exists(".runtime/status.json"):
        with open('.runtime/status.json', 'w') as outfile:
            init_data = {
                "kind": {
                    "status": "unavailable"
                },
                "ui": {
                    "status": "unavailable"
                },
                "workflow-engine": {
                    "status": "unavailable"
                },
                "python-executor": {
                    "status": "unavailable"
                },
                "admin-service": {
                    "status": "unavailable"
                }
            }
            json.dump(init_data, outfile)


def write_status(service, status):
    with open('.runtime/status.json', 'r') as json_file:
        data = json.load(json_file)
        data[service]["status"] = status
    with open('.runtime/status.json', 'w') as output_file:
        json.dump(data, output_file)


def health_check():
    for service in SERVICES:
        try:
            print(service)
            r = requests.get("http://{}:8080/health".format(service), timeout=1)
            status = r.json()["status"]
        except Exception as e:
            status = "unavailable"
        write_status(service, status)


def watcher():
    init_status()
    while True:
        health_check()
        time.sleep(2)


if __name__ == "__main__":
    watcher()
