# utils.py
from bloom_filter import BloomFilter
from models import Server
import yaml, os, random, sqlite3

database = "database/test.db"

def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def transform_backends_from_config(config):
    register = {}
    for entry in config.get('hosts', []):
        register.update({entry["host"]: [Server(endpoint) for endpoint in entry["servers"]]})
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
    conn = sqlite3.connect(database) 
    cursor = conn.execute("SELECT email, password from USERS")
    bloom = BloomFilter()
    for row in cursor:
        bloom.add(row[0])
    conn.close()
    return bloom

def check_user(email, password, bloom):
    if email not in bloom:
        return 401
    else:
        conn = sqlite3.connect(database) 
        cursor = conn.execute("SELECT * FROM USERS WHERE email = '" + email + "';")

        for row in cursor:
            if(row[1] == password):
                conn.close()
                return 200
            else:
                conn.close()
                return 401
    return 401

def welcome(register):
    print("\n")
    print('\033[1m' + "Running server health-checkup protocol:" + '\033[0m')
    for server in register:
        print("Host: ", server)
        print("Servers: " + str(register[server]) + "\n")
    
def refresh_stats(register):
    f = open("logs/status.txt", "w")
    for host in register:
        for server in register[host]:
            f.write(str(host) + " " + str(server.endpoint) + " " + str(server.healthy) + " " + str(server.open_connections)+"\n")
    f.close()

def log_file(message):
    log = open("logs/log.txt", "a")
    log.write(message)
    log.close()

def process_firewall_rules_flag(config, host, client_ip):
    for entry in config.get('hosts', []):
        if host == entry['host']:
            firewall_rules = entry.get('firewall_rules', {})
            if client_ip in firewall_rules.get("ip_reject", []):
                return False
    return True