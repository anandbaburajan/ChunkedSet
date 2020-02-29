from flask import Flask, request, jsonify, abort
import requests

app2 = Flask(__name__)

class Chunk():
    N = 9   #Max size of ChunkedSet
    def __init__(self, name, size):
        self.name = name   #Name of chunk
        self.size = size   #Max capacity of chunk (k)
        self.data = set()   #Numbers stored in a set, implemented as a hashtable

@app2.route("/api/insert/", methods=['POST'])   #Endpoint for inserting a number
def insert():
    if not request.json or not 'num' in request.json:
        abort(400)   #If request body is incorrect
    num = request.json['num']   #Retrieve number from request
    if 'ready' in request.json and request.json['ready']:   #Direct request to insert from another chunk
        B.data.add(num)   #Add num to the chunk
        return jsonify({'response': 'Successfully Inserted!'})
    size2 = len(B.data)
    url_size_1 = 'http://localhost:8001/api/get_chunk_size'
    s1 = requests.get(url_size_1).json()
    url_size_3 = 'http://localhost:8003/api/get_chunk_size'
    s3 = requests.get(url_size_3).json()
    url_size = 'http://localhost:8002/api/get_size'   #To get size of chunks and total number of elements
    jsonsize = requests.get(url_size).json()
    size1 = s1['chunk_size']
    size3 = s3['chunk_size']
    total = jsonsize['total']
    if total<Chunk.N:   #If there's space left to insert
        if num in B.data:
            return jsonify({'response': 'Failed!'})   #If num is already in B
        url_pres_1 = 'http://localhost:8001/api/present'   #To check presence in A
        p1 = requests.post(url_pres_1, json = {'num': num}).json()
        url_pres_3 = 'http://localhost:8003/api/present'   #To check presence in C
        p3 = requests.post(url_pres_3, json = {'num': num}).json()
        if p1['present'] or p3['present']:
            return jsonify({'response': 'Failed!'})   #If num is already in A or C
        if size2 < k:
            B.data.add(num)   #Add num to B if not full
            return jsonify({'response': 'Successfully Inserted!'})
        if size1 < k:   #If A is not full
            url_ins_1 = 'http://localhost:8001/api/insert'
            i1 = requests.post(url_ins_1, json = {'num': num, 'ready':1}).json()   #Directly add num to A
            return jsonify({'response': i1['response']})
        if size3 < k:   #If C is not full
            url_ins_3 = 'http://localhost:8003/api/insert'
            i3 = requests.post(url_ins_3, json = {'num': num, 'ready':1}).json()   #Directly add num to C
            return jsonify({'response': i3['response']})
    else:
        return jsonify({'response': 'Failed!'})

@app2.route("/api/present/", methods=['POST'])   #Endpoint for checking presence of a number
def present():
    num = request.json['num']   #Retrieve number from request
    if num in B.data:
        return jsonify({'present': 1})   #If element already exists
    return jsonify({'present': 0})

@app2.route("/api/get_chunk_size", methods=['GET'])   #Endpoint for getting current size of chunk
def get_chunk_size():
    return jsonify({'chunk_size': len(B.data)})

@app2.route("/api/get_size", methods=['GET'])   #Endpoint for getting total elements
def get_size():
    s2 = len(B.data)
    url_size_1 = 'http://localhost:8001/api/get_chunk_size'
    s1 = requests.get(url_size_1).json()
    url_size_3 = 'http://localhost:8003/api/get_chunk_size'
    s3 = requests.get(url_size_3).json()
    total = s2 + s1['chunk_size'] + s3['chunk_size']
    return jsonify({'total': total})

@app2.route("/api/clear", methods=['POST'])   #Endpoint for clearing all chunks
def clear():
    if request.json and 'ready' in request.json and request.json['ready']:   #Direct request to clear from another chunk
        B.data = set()
        return jsonify({'response': 'Cleared!'})
    B.data = set()
    url_clear_1 = 'http://localhost:8001/api/clear'
    c1 = requests.post(url_clear_1, json = {'ready':1}).json()
    url_clear_3 = 'http://localhost:8003/api/clear'
    c3 = requests.post(url_clear_3, json = {'ready':1}).json()
    return jsonify({'response': 'Cleared!'})

if __name__ == '__main__':
    k=3
    B = Chunk("B",k)   #New chunk with max capacity 3
    app2.run(port=8002)
