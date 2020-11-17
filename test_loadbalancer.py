# test_loadbalancer.py
from loadbalancer import loadbalancer
from joblib import Parallel, delayed
import pytest
import multiprocessing
import re
import random

emails = ["akzelxw@hotmail.com","elum@gmail.com","akbar.ca","akaterasu@gmail.com","akarui.kibuno@gmail.com","ajsparkchick@hotmail.com","ajmeia@yahoo.com","ajhnstn87@gmail.com","ailuvzhoko4@hotmail.com","ailuvzhoko3@hotmail.com","ailuvzhoko2@hotmail.com","ailuvzhoko@hotmail.com","aillensiquioco@aol.com","ahmovic_ines@hotmail.com","ahmed_g300@yahoo.com","ahmadjazlan@gmail.com","ahmad_ridho19@yahoo.com","ahgou_9@hotmail.com","ahan221@yahoo.com","agungarifiyanto@yahoo.com","agnestenerife@yahoo.com","agian_ee@yahoo.com","afrodzac007@aol.com","affinboy@hotmail.com","afdal_hair1303@yahoo.com","afd1944@gmail.com","afandi.ilham@yahoo.com","aerongreg@yahoo.com","adria@jbi.com","ado97_madero@hotmail.com","aditye55@yahoo.com","adhie.impossible@gmail.com","adeeldaftary@gmail.com","adam_petre@hotmail.com","adam_khaldoon911@yahoo.com","ium@yahoo.com"]

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_mango(client):
    print("\n\n\033[1mBulk requests for www.mango.com \033[0m")
    def execute(i):
        result = client.get('/', headers={"Host":"www.mango.com"})

    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(10))

# def test_host_routing_mango_login(client):
#     print("\n\n\033[1mBulk requests for www.mango.com/login \033[0m")
#     def execute(i):
#         result = client.get('/login', headers={"Host":"www.mango.com", "email": emails[i], "password": emails[i + random.randint(-1,0)].split("@")[0]})

#     Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(execute)(i) for i in range(len(emails)))

# def test_host_routing_mango_login(client):
#     def func(i):
#         result = client.get('/', headers={"Host":"www.mango.com", "email":"akzelxw@hotmail.com", "password":"qwerty"})
#         # print(result.data.decode('utf-8'))
#         # assert re.match("This is the mango application. Serving on localhost:\d+.", result.data.decode('utf-8')) != None
#         # print(result.data)
#     Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(func)(i) for i in range(10))
# def test_host_routing_apple(client):
#     result = client.get('/', headers={"Host":"www.apple.com"})
#     print(result.data)
#     assert b'This is the apple application. Serving on localhost:9082.' == result.data

# def test_host_routing_notfound(client):
#     result = client.get('/', headers={"Host":"www.notmango.com"})
#     assert b'Not Found' in result.data
#     assert 404 == result.status_code

# def test_server_bad_servers(client):
#     result = client.get('/', headers={"Host":"www.apple.com"})
#     assert b'This is the apple application. Serving on localhost:9082.' == result.data

# def test_server_no_servers(client):
#     result = client.get('/', headers={"Host":"www.orange.com"})
#     assert 503 == result.status_code

# def test_path_routing_mango(client):
#     result = client.get('/mango')
#     print("This is the mango application. Serving on localhost:\d+.", result.data.decode('utf-8'))
#     assert re.match("This is the mango application. Serving on localhost:\d+.", result.data.decode('utf-8')) != None

# def test_path_routing_apple(client):
#     result = client.get('/apple')
#     assert b'This is the apple application. Serving on localhost:9082.' == result.data

# def test_path_routing_notfound(client):
#     result = client.get('/notmango')
#     assert b'Not Found' in result.data
#     assert 404 == result.status_code