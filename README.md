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
python app.py
```

Use Postman or your any tool of your for API testing

Endpoints
------------

```bash
http://localhost:5000/api/insert/     #Post request JSON body format: {"num":1}
http://localhost:5000/api/get_size/
http://localhost:5000/api/remove/     #Post request JSON body format: {"num":1}
http://localhost:5000/api/clear/
```
