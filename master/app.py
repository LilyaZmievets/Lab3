import redis 
import zmq
from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	fibonacciNumber = int(DataBaseConn.lindex("fibonacciNumber", 0))
	Res = "Current Fibonacci num  = " + str(fibonacciNumber) + " ."
	return Res

@app.route('/', methods = ['POST'])
def Inq():
	Cont = zmq.Context()
	socket = Cont.socket(zmq.REQ)
	socket.connect("tcp://worker:5555")
	socket.send('poking workers...')	
	curFib = socket.recv()
	return "Increase done"
	
if __name__ == "__main__":
    DataBaseConn = redis.Redis('redis')
    try:
        DataBaseConn.ping()
    except redis.ConnectionError:
        print('Can't connect to database')
    if(int (DataBaseConn.llen("fibonacciNumber")) == 0):
        DataBaseConn.rpush("fibonacciNumber", 2, 1)
     
app.run(host="0.0.0.0", debug=True)
