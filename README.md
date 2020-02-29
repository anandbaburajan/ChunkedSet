# ChunkedSet
Implement a ChunkedSet - which is a set of size N that can store upto N unique numbers. The ChunkedSet stores its elements in Chunks of a fixed sized k.

The various operations such as insert, remove, get_size etc.. are always performed on a chunk object. The chunks themselves may be placed on different computers in a network hence for each of the operations, one Chunk must corrdinate with other chunks to ensure that the overall ChunkedSet is valid.


Installation
------------

```bash
pip install -r requirements.txt
```

How to run?
------------

```bash
python app1.py
python app2.py
python app3.py
```

Use Postman or any tool of your choice for API testing

Endpoints
------------
Chunk A (Port: 8001), Chunk B (Port: 8002) and Chunk C (Port: 8003)

```bash
http://localhost:port/api/insert/     #Post request JSON body format: {"num":1}
http://localhost:port/api/get_size/
http://localhost:port/api/remove/     #Post request JSON body format: {"num":1}
http://localhost:port/api/clear/
```
