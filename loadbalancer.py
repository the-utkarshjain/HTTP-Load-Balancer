# loadbalancer.py
from flask import Flask, request
import requests, random
from utils import *
import threading 
import time
import sys

lock = threading.Lock()
loadbalancer = Flask(__name__)
config = load_configuration('loadbalancer.yaml')
register = transform_backends_from_config(config)
bloom = train_bloom_filter()
updated_register = healthcheck(register)
welcome(updated_register)

@loadbalancer.route("/")
@loadbalancer.route("/<path>")
def router(path="/"):
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
    # auth = request.headers["Auth"]
    # if auth in bloom:
    #     print(auth)
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                return "No Backends servers available for" + host_header, 503

            lock.acquire()
            healthy_server.open_connections += 1
            # refresh_stats(register)
            # time.sleep(1)
            print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))

            lock.acquire()
            healthy_server.open_connections -= 1
            # refresh_stats(register)
            print("Request processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
            lock.release()
            return response.content, response.status_code
    
    for entry in config["paths"]:
        if ("/" + path) == entry["path"]:
            healthy_server = get_healthy_server(entry["path"], register)
            if not healthy_server:
                return "No Backends servers available for /" + path, 503
            
            lock.acquire()
            healthy_server.open_connections += 1
            print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))
            
            lock.acquire()
            healthy_server.open_connections -= 1
            print("Request for /" + path + " processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
            lock.release()
            return response.content, response.status_code

    return "Not Found", 404
