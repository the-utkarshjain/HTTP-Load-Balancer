# app.py
# Serves all the servers

from flask import Flask
import os, time
from random import randint
import requests

app = Flask(__name__)

@app.route('/')
def sample():
    time.sleep(randint(3,10))
    return "This is the {} application. Serving on {}.".format(os.environ["APP"], os.environ["ENDPOINT"])
    
@app.route('/healthcheck')
def healthcheck():
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)