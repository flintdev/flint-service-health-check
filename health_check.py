import requests
import time
import json
import os
import socket

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


def check_ui():
    if check_ui_port(8000):
        status = "available"
    else:
        status = "unavailable"
    return status


def check_ui_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('ui', port)) == 0


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
            if service == "ui":
                status = check_ui()
            else:
                r = requests.get("http://{}:8080/health".format(service), timeout=1)
                try:
                    status = r.json()["status"]
                except Exception as e:
                    status = r.json()["Status"]
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
