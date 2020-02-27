from flask import Flask, request, jsonify, abort

app = Flask(__name__)

class Chunk():   #Each chunk on a different computer
    total_elements = 0   #Total number of unique numbers in ChunkedSet
    def __init__(self, name, size):
        self.name = name   #Name of chunk
        self.size = size   #Max capacity of chunk (k)
        self.data = set()   #Numbers stored in a set, implemented as a hashtable

@app.route("/api/insert/", methods=['POST'])   #Endpoint for inserting a number
def insert():   #Post request JSON body format: {"num":1}
    if not request.json or not 'num' in request.json:
        abort(400)
    num = request.json['num']   #Retrieve number from request
    if Chunk.total_elements<N:   #If there's space left to insert
        for x in chunks:   #For each chunk
             if num in x.data:   #Check if num is already there in the chunk
                return jsonify({'response': 'Failed!'})
        cur_chunk = min(chunks, key=lambda x: len(x.data))   #Choose smallest chunk
        if len(cur_chunk.data) == k:   #Check if the chunk is full
            return jsonify({'response': 'Failed!'})
        cur_chunk.data.add(num)   #Add num to the chunk
        Chunk.total_elements += 1   #Update total elements
        return jsonify({'response': 'Successfully Inserted!'})
    else:
        return jsonify({'response': 'Failed!'})

@app.route("/api/get_size", methods=['GET'])   #Endpoint for getting total elements
def get_size():
    return jsonify({'total_elements': Chunk.total_elements})

if __name__ == '__main__':
    N = 9   #ChunkedSet of size
    k = 3   #Maximum capacity of a chunk
    A = Chunk("A",k)   #New chunk
    B = Chunk("B",k)
    C = Chunk("C",k)
    chunks = [A,B,C]   #Iterable for chunks
    app.run()
