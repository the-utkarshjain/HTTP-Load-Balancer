# test_loadbalancer.py
import sys
sys.path.append('./src')
from loadbalancer import loadbalancer
from utils import log_file
from joblib import Parallel, delayed
import pytest, multiprocessing, random

emails = ["akzelxw@hotmail.com","elum@gmail.com","akbar.ca","akaterasu@gmail.com","akarui.kibuno@gmail.com","ajsparkchick@hotmail.com","ajmeia@yahoo.com","ajhnstn87@gmail.com","ailuvzhoko4@hotmail.com","ailuvzhoko3@hotmail.com","ailuvzhoko2@hotmail.com","ailuvzhoko@hotmail.com","aillensiquioco@aol.com","ahmovic_ines@hotmail.com","ahmed_g300@yahoo.com","ahmadjazlan@gmail.com","ahmad_ridho19@yahoo.com","ahgou_9@hotmail.com","ahan221@yahoo.com","agungarifiyanto@yahoo.com","agnestenerife@yahoo.com","agian_ee@yahoo.com","afrodzac007@aol.com","affinboy@hotmail.com","afdal_hair1303@yahoo.com","afd1944@gmail.com","afandi.ilham@yahoo.com","aerongreg@yahoo.com","adria@jbi.com","ado97_madero@hotmail.com","aditye55@yahoo.com","adhie.impossible@gmail.com","adeeldaftary@gmail.com","adam_petre@hotmail.com","adam_khaldoon911@yahoo.com","ium@yahoo.com"]
ip_list = ["157.25.45.15", "75.59.142.45", "156.56.245.136", "192.168.29.142", "47.125.74.69", "252.46.86.13", "184.236.45.96", "136.254.214.45", "125.59.27.36", "231.35.24.82"]
bulk = 10
@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_amazon(client):
    host = "www.amazon.com"
    print("\n\n\033[1mBulk requests for "+ host +" \033[0m")
    log_file("\n\nBulk requests for "+ host +"\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(bulk))

def test_firewall_amazon(client):
    host = "www.amazon.com"
    print("\n\n\033[1mBulk firewall requests for "+ host +" \033[0m")
    log_file("\n\nBulk firewall requests for "+ host +"\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host}, environ_base={'REMOTE_ADDR': ip_list[i]})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(len(ip_list)))

def test_host_routing_amazon_login(client):
    host = "www.amazon.com"
    print("\n\n\033[1mTesting bloom filter with bulk requests for "+ host +"/login \033[0m")
    log_file("\n\nTesting bloom filter with bulk requests for "+ host +"/login\n\n")
    def execute(i):
        result = client.get('/login', headers={"Host":host, "email": emails[i], "password": emails[i + random.randint(-1,0)].split("@")[0]}, environ_base={'REMOTE_ADDR': ip_list[i%len(ip_list)]})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(len(emails)))

def test_host_routing_apple(client):
    host = "www.apple.com"
    print("\n\n\033[1mBulk requests for "+ host+ " \033[0m")
    log_file("\n\nBulk requests for "+ host+ "\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(bulk))

def test_firewall_apple(client):
    host = "www.apple.com"
    print("\n\n\033[1mBulk firewall requests for "+ host +" \033[0m")
    log_file("\n\nBulk firewall requests for "+ host +"\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host}, environ_base={'REMOTE_ADDR': ip_list[i]})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(len(ip_list)))

def test_host_routing_apple_login(client):
    host = "www.apple.com"
    print("\n\n\033[1mTesting bloom filter with bulk requests for "+ host +"/login \033[0m")
    log_file("\n\nTesting bloom filter with bulk requests for "+ host +"/login\n\n")
    def execute(i):
        result = client.get('/login', headers={"Host":host, "email": emails[i], "password": emails[i + random.randint(-1,0)].split("@")[0]}, environ_base={'REMOTE_ADDR': ip_list[i%len(ip_list)]})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(len(emails)))

def test_host_notfound(client):
    host = "www.notamazon.com"
    print("\n\n\033[1mBulk requests for "+ host +" \033[0m")
    log_file("\n\nBulk requests for "+ host +"\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(bulk))

def test_server_no_servers(client):
    host = "www.flipkart.com"
    print("\n\n\033[1mBulk requests for "+ host +" \033[0m")
    log_file("\n\nBulk requests for "+ host +"\n\n")
    def execute(i):
        result = client.get('/', headers={"Host":host})
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(bulk))

