# HTTP-Load-Balancer
A Load Balancer is a networking component for distributing load across multiple servers used to horizontally scale web based applications. 
There are many popular ones out there such as NGINX, HAProxy, Traefik to name a few. However, we haven't used any of those load balancer but instead we have built the functinality ourselves.
<br /> **Ques: Why do Load Balancers play a big part in networking infrastructure?** <br />
Ans: Because they allow engineers to scale and improve reliability of web applications.

## Installation guide
1. Install and run the docker daemon.  
2. Open a terminal and run: git clone ```https://github.com/the-utkarshjain/HTTP-Load-Balancer.git```
3. Navigate inside the folder named **HTTP Load Balancer** and run the following commands:
```console
$ conda create -n loadbalancer --file package-list.txt
$ conda activate loadbalancer
$ python gui.py
$ make
```
## Directions
1. The GUI shows the real time health of all the servers along with the load on each of them.
2. On the second tab, press `Generate logs` to see which request was redirected to which server and status code of each request.
