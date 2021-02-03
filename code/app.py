# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:35:59 2021

@author: reuben_sinha
"""

from flask import Flask, render_template, request
import redis
import json
import sys

app = Flask(__name__)

with open('env.json') as f:
  data = json.load(f)

def connect(host, password, port):
    r = redis.Redis(host=host, password=password, port=port)
    #r = "Dummy"
    return r

#redis_conn = connect(data["host"], data["password"], data["port"])
redis_conn = connect(sys.argv[1], sys.argv[3], sys.argv[2])

#Home page
@app.route('/') 
def index():
    all_keys = redis_conn.keys()
    package = {}
    for byte_key in all_keys:
        key = byte_key.decode('utf-8')
        package[key] = {}
        try:
            for k,v in redis_conn.hgetall(key).items():
                package[key][k.decode('utf-8')] = v.decode('utf-8')
        except Exception as  e:
            print(e)
    
    #dummy_data = {"Linkedin": {"Rueben":"pass1", "India": "Hihewi"}, "Yahoo":{"qwqw": "wewe"}}
    
    return render_template('index.html', data=package)

#Ceate entries
@app.route("/create", methods=['POST'])
def create():
    data = request.form
    print("Hset data",data)
    redis_conn.hset(data["account"],data["username"],data["password"])
    return {"status": "success"}

#Delete the Entires
@app.route("/delete", methods=['DELETE'])
def delete():
    data = request.form
    print("Deleting key", data["account"])
    redis_conn.delete(data["account"])
    return {"status": "success"}

app.run(host="0.0.0.0", port="6000")
