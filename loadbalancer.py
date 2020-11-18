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

            lock.acquire()
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                lock.release()
                send_back_msg = "No Backends servers available for" + host_header + ". ERROR CODE 503"
                print(send_back_msg)
                log_file(send_back_msg + "\n")
                return send_back_msg, 503
            healthy_server.open_connections += 1
            refresh_stats(updated_register)
            send_back_msg = "Delegated to: " + str(healthy_server.endpoint) + ". Open connections: " + str(healthy_server.open_connections) + ". STATUS CODE 202"
            print(send_back_msg)
            log_file(send_back_msg + "\n")
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))

            lock.acquire()
            healthy_server.open_connections -= 1
            refresh_stats(updated_register)
            send_back_msg = "Request processed: " + str(healthy_server.endpoint) + ". Open connections: " + str(healthy_server.open_connections) + ". STATUS CODE 200"
            print(send_back_msg)
            log_file(send_back_msg + "\n")
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

    send_back_msg = "This site can’t be reached " + host_header + ". Server IP address could not be found. ERROR CODE 404"
    print(send_back_msg)
    log_file(send_back_msg + "\n")
    return "Not Found", 404

@loadbalancer.route("/login")
def router_login():
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
        
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                send_back_msg = "No Backends servers available for" + host_header + ". ERROR CODE 503"
                print(send_back_msg)
                log_file(send_back_msg + "\n")
                return send_back_msg, 503

            if(request.headers["email"]):
                status_check = check_user(request.headers["email"], request.headers["password"], bloom)
                if(status_check == 401):
                    send_back_msg = request.headers["email"] + " not found. ERROR CODE 401"
                    print(send_back_msg)
                    log_file(send_back_msg + "\n")
                    return 401
                else:
                    send_back_msg = "Welcome " + request.headers["password"] + ". Your request is being processed. STATUS CODE 202"
                    print(send_back_msg)
                    log_file(send_back_msg + "\n")

            lock.acquire()
            healthy_server.open_connections += 1
            refresh_stats(updated_register)
            send_back_msg = "Delegated to: " + str(healthy_server.endpoint) + ". Open connections: " + str(healthy_server.open_connections) + ". STATUS CODE 202"
            print(send_back_msg)
            log_file(send_back_msg + "\n")
            lock.release()

            response = requests.get("http://{}".format(healthy_server.endpoint))

            lock.acquire()
            healthy_server.open_connections -= 1
            refresh_stats(updated_register)
            send_back_msg = "Request processed:" + str(healthy_server.endpoint) + ". Open connections: " + str(healthy_server.open_connections) + ". STATUS CODE 200"
            print(send_back_msg)
            log_file(send_back_msg + "\n")
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

    send_back_msg = "This site can’t be reached " + host_header + ". Server IP address could not be found. ERROR CODE 404"
    print(send_back_msg)
    log_file(send_back_msg + "\n")
    return "Not Found", 404