# Fibonacci-Calculator

## Usage
- Install project dependencies
```bash
# Install protobuf compiler
sudo apt-get install protobuf-compiler

# Install buildtools
sudo apt-get install build-essential make

# Install grpc packages
pip3 install -r requirements.txt
```
- Compile protobuf schema to python wrapper
```bash
cd django-rest-tutorial && make
cd ../gRPC-with-protobuf && make
cd ../eclipse-mosquitto && make
```
- Run the eclipse mosquitto docker container
```bash
docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
- Start the loggin service
```bash
$ python3 server.py
```
- Start the fibonacci calculator service
```bash
# open another terminal
cd gRPC-with-protobuf
python3 server.py
```

- Start the REST server
```bash
# open another terminal
cd django-rest-tutorial/mysite 
python3 manage.py migrate
python3 manage.py runserver
```

- POST method
```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/rest/fibonacci/ -d "{\"order\": 3}"
'''
you would get
{"order":3,"value":2}
'''
```
- GET method
```bash
curl http://localhost:8000/rest/logs
'''
you would get
{"history":[{"order":3,"value":2,"id":0}]}
'''
```