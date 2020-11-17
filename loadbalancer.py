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
def router(path="/"):
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
        
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                print("No Backends servers available for" + host_header)
                return "No Backends servers available for" + host_header, 503

            lock.acquire()
            healthy_server.open_connections += 1
            print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))

            lock.acquire()
            healthy_server.open_connections -= 1
            print("Request processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
            lock.release()
            return response.content, response.status_code
    
    # for entry in config["paths"]:
    #     if ("/" + path) == entry["path"]:
    #         healthy_server = get_healthy_server(entry["path"], register)
    #         if not healthy_server:
    #             print("No Backends servers available for" + host_header)
    #             return "No Backends servers available for /" + path, 503
            
    #         lock.acquire()
    #         healthy_server.open_connections += 1
    #         print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
    #         lock.release()

    #         response = requests.get("http://{}".format(healthy_server.endpoint))
            
    #         lock.acquire()
    #         healthy_server.open_connections -= 1
    #         print("Request for /" + path + " processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
    #         lock.release()
    #         return response.content, response.status_code

    print("This site can’t be reached. " + host_header + " server IP address could not be found.")
    return "Not Found", 404

@loadbalancer.route("/login")
def router_login():
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
        
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                print("No Backends servers available for" + host_header)
                return "No Backends servers available for" + host_header, 503

            if(request.headers["email"]):
                status_check = check_user(request.headers["email"], request.headers["password"], bloom)
                if(status_check == 401):
                    print(request.headers["email"] + " is wrong. Sign up to create a new account.")
                    return 401
                else:
                    print("Welcome " + request.headers["password"] + ". Your request is being processed.")

            lock.acquire()
            healthy_server.open_connections += 1
            print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))

            lock.acquire()
            healthy_server.open_connections -= 1
            print("Request processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
            lock.release()
            return response.content, response.status_code
    
    # for entry in config["paths"]:
    #     if ("/" + path) == entry["path"]:
    #         healthy_server = get_healthy_server(entry["path"], register)
    #         if not healthy_server:
    #             print("No Backends servers available for" + host_header)
    #             return "No Backends servers available for /" + path, 503
            
    #         lock.acquire()
    #         healthy_server.open_connections += 1
    #         print("Request delegated to: " + str(healthy_server.endpoint) + " with " + str(healthy_server.open_connections))
    #         lock.release()

    #         response = requests.get("http://{}".format(healthy_server.endpoint))
            
    #         lock.acquire()
    #         healthy_server.open_connections -= 1
    #         print("Request for /" + path + " processed by " + str(healthy_server.endpoint) + ". Updated open connections: " + str(healthy_server.open_connections))
    #         lock.release()
    #         return response.content, response.status_code

    print("This site can’t be reached. " + host_header + " server IP address could not be found.")
    return "Not Found", 404