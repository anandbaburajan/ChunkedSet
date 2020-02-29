from flask import Flask, request, jsonify, abort
import requests

app1 = Flask(__name__)

class Chunk():
    N = 9   #Max size of ChunkedSet
    def __init__(self, name, size):
        self.name = name   #Name of chunk
        self.size = size   #Max capacity of chunk (k)
        self.data = set()   #Numbers stored in a set, implemented as a hashtable

@app1.route("/api/insert/", methods=['POST'])   #Endpoint for inserting a number
def insert():
    if not request.json or not 'num' in request.json:
        abort(400)   #If request body is incorrect
    num = request.json['num']   #Retrieve number from request
    if 'ready' in request.json and request.json['ready']:   #Direct request to insert from another chunk
        A.data.add(num)   #Add num to the chunk
        return jsonify({'response': 'Successfully Inserted!'})
    size1 = len(A.data)
    url_size_2 = 'http://localhost:8002/api/get_chunk_size'
    s2 = requests.get(url_size_2).json()
    url_size_3 = 'http://localhost:8003/api/get_chunk_size'
    s3 = requests.get(url_size_3).json()
    url_size = 'http://localhost:8001/api/get_size'   #To get size of chunks and total number of elements
    jsonsize = requests.get(url_size).json()
    size2 = s2['chunk_size']
    size3 = s3['chunk_size']
    total = jsonsize['total']
    if total<Chunk.N:   #If there's space left to insert
        if num in A.data:
            return jsonify({'response': 'Failed!'})   #If num is already in A
        url_pres_2 = 'http://localhost:8002/api/present'   #To check presence in B
        p2 = requests.post(url_pres_2, json = {'num': num}).json()
        url_pres_3 = 'http://localhost:8003/api/present'   #To check presence in C
        p3 = requests.post(url_pres_3, json = {'num': num}).json()
        if p2['present'] or p3['present']:
            return jsonify({'response': 'Failed!'})   #If num is already in B or C
        if size1 < k:
            A.data.add(num)   #Add num to A if not full
            return jsonify({'response': 'Successfully Inserted!'})
        if size2 < k:   #If B is not full
            url_ins_2 = 'http://localhost:8002/api/insert'
            i2 = requests.post(url_ins_2, json = {'num': num, 'ready':1}).json()   #Directly add num to B
            return jsonify({'response': i2['response']})
        if size3 < k:   #If C is not full
            url_ins_3 = 'http://localhost:8003/api/insert'
            i3 = requests.post(url_ins_3, json = {'num': num, 'ready':1}).json()   #Directly add num to C
            return jsonify({'response': i3['response']})
    else:
        return jsonify({'response': 'Failed!'})

@app1.route("/api/present/", methods=['POST'])   #Endpoint for checking presence of a number
def present():
    num = request.json['num']   #Retrieve number from request
    if num in A.data:
        return jsonify({'present': 1})   #If element already exists
    return jsonify({'present': 0})

@app1.route("/api/get_chunk_size", methods=['GET'])   #Endpoint for getting current size of chunk
def get_chunk_size():
    return jsonify({'chunk_size': len(A.data)})

@app1.route("/api/get_size", methods=['GET'])   #Endpoint for getting total elements
def get_size():
    s1 = len(A.data)
    url_size_2 = 'http://localhost:8002/api/get_chunk_size'
    s2 = requests.get(url_size_2).json()
    url_size_3 = 'http://localhost:8003/api/get_chunk_size'
    s3 = requests.get(url_size_3).json()
    total = s1 + s2['chunk_size'] + s3['chunk_size']
    return jsonify({'total': total})

if __name__ == '__main__':
    k=3
    A = Chunk("A",k)   #New chunk with max capacity 3
    app1.run(port=8001)
