# test_loadbalancer.py
from loadbalancer import loadbalancer
from joblib import Parallel, delayed
import pytest
import multiprocessing
import re

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client

def test_host_routing_mango(client):
    print("Serving requestes for www.mango.com")
    def func(i):
        result = client.get('/', headers={"Host":"www.mango.com"})
        # print(result.data.decode('utf-8'))
        # assert re.match("This is the mango application. Serving on localhost:\d+.", result.data.decode('utf-8')) != None
        # print(result.data)
    Parallel(n_jobs= multiprocessing.cpu_count(), backend = 'threading')(delayed(func)(i) for i in range(10))

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