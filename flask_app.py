
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import json
import math
import sympy
import binascii as bs

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/api/get-prime', methods = ['GET', 'POST'])
def handle_get_prime():
    # ?n=###
    p = 0
    arg1 = str(request.args.get('n'))
    if arg1.isdigit():
        n = int(arg1)
        p = sympy.randprime(10**n, 10**(n+1)) if n > 0 else 0

    data_set = {'p': str(p)}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/api/get-mod', methods = ['GET', 'POST'])
def handle_get_mod():
    # ?p1=###&p2=###
    mod = 0
    arg1 = str(request.args.get('p1'))
    arg2 = str(request.args.get('p2'))
    if arg1.isdigit() and arg2.isdigit():
        p1 = int(arg1)
        p2 = int(arg2)
        if (p1 > 2) and (p2 > 2):
            mod = p1 * p2

    data_set = {'mod': str(mod)}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/api/get-dkey', methods = ['GET', 'POST'])
def handle_get_dkey():
    # ?p1=###&p2=###&ekey=###
    dkey = 0
    arg1 = str(request.args.get('p1'))
    arg2 = str(request.args.get('p2'))
    arg3 = str(request.args.get('ekey'))
    if arg1.isdigit() and arg2.isdigit() and arg3.isdigit():
        p1 = int(arg1)
        p2 = int(arg2)
        ekey = int(arg3)
        if (p1 > 2) and (p2 > 2):
            lamb = math.lcm(p1-1,p2-1)
            dkey = pow(ekey, -1, lamb)

    data_set = {'dkey': str(dkey)}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/api/encrypt', methods = ['GET', 'POST'])
def handle_encrypt():
    # ?msg=###&ekey=###&mod=###
    cipher = ''
    arg1 = str(request.args.get('msg'))
    arg2 = str(request.args.get('ekey'))
    arg3 = str(request.args.get('mod'))
    if arg2.isdigit() and arg3.isdigit() and (len(arg1) > 0):
        ekey = int(arg2)
        mod = int(arg3)
        if (ekey > 2) and (mod > 2):
            msg = bs.hexlify(arg1.encode()).decode()
            cipher = pow(int(msg,16),ekey,mod)

    data_set = {'cipher': str(cipher)}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/api/decrypt', methods = ['GET', 'POST'])
def handle_decrypt():
    # ?cipher=###&dkey=###&mod=###
    msg = ''
    arg1 = str(request.args.get('cipher'))
    arg2 = str(request.args.get('dkey'))
    arg3 = str(request.args.get('mod'))
    if arg1.isdigit() and arg2.isdigit() and arg3.isdigit():
        cipher = int(arg1)
        dkey = int(arg2)
        mod = int(arg3)
        if (dkey > 2) and (mod > 2):
            decipher = pow(cipher,dkey,mod)
            try:
                msg = bytearray.fromhex(hex(decipher)[2:]).decode()
            except:
                msg = ''

    data_set = {'msg': str(msg)}
    json_dump = json.dumps(data_set)

    return json_dump

