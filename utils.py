# utils.py
from models import Server
import yaml, os
import random
import sqlite3
from bloom_filter import BloomFilter

def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def transform_backends_from_config(config):
    register = {}
    for entry in config.get('hosts', []):
        register.update({entry["host"]: [Server(endpoint) for endpoint in entry["servers"]]})
    for entry in config.get('paths', []):
        register.update({entry["path"]: [Server(endpoint) for endpoint in entry["servers"]]})
    return register

def get_healthy_server(host, register):
    try:
        return least_connections([server for server in register[host] if server.healthy])
    except IndexError:
        return None

def least_connections(servers):
    if not servers:
        return None
    return min(servers, key=lambda x: x.open_connections)

def healthcheck(register):
    for host in register:
        for server in register[host]:
            server.healthcheck_and_update_status()
    return register

def train_bloom_filter():
    conn = sqlite3.connect('test.db') 
    cursor = conn.execute("SELECT email, password from USERS")
    bloom = BloomFilter()
    for row in cursor:
        bloom.add(row[0])
    return bloom

def welcome(register):
    print("\n")
    print('\033[1m' + "Running server health-checkup protocol:" + '\033[0m')
    for server in register:
        print("Host: ", server)
        print("Servers: " + str(register[server]) + "\n")
    
def refresh_stats(register):
    os.system('cls' if os.name == 'nt' else 'clear')
    for host in register:
        for server in register[host]:
            print(server.endpoint, server.open_connections)