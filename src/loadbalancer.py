# loadbalancer.py
from utils import *
from flask import Flask, request
import requests, random, threading, time, os

lock = threading.Lock()
loadbalancer = Flask(__name__)
config = load_configuration('config/loadbalancer.yaml')
register = transform_backends_from_config(config)
bloom = train_bloom_filter()
updated_register = healthcheck(register)
welcome(updated_register)

@loadbalancer.route("/")
def router(path="/"):
    updated_register = healthcheck(register)
    host_header = request.headers["Host"]
    if not process_firewall_rules_flag(config, host_header, request.environ["REMOTE_ADDR"]):
        print("Request blocked for ip: " + request.environ["REMOTE_ADDR"] + ". STATUS CODE 403")
        return "Forbidden", 403
        
    for entry in config["hosts"]:
        if host_header == entry["host"]:
            lock.acquire()
            healthy_server = get_healthy_server(entry["host"], updated_register)
            if not healthy_server:
                lock.release()
                send_back_msg = host_header + " is unable to handle requests. ERROR CODE 503"
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

    send_back_msg = "This site can’t be reached: " + host_header + ". Server IP address could not be found. ERROR CODE 404"
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
                send_back_msg = host_header + " is unable to handle requests. ERROR CODE 503"
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

    send_back_msg = "This site can’t be reached: " + host_header + ". Server IP address could not be found. ERROR CODE 404"
    print(send_back_msg)
    log_file(send_back_msg + "\n")
    return "Not Found", 404