import redis 
import zmq
from flask import Flask

app = Flask(__name__)

conn = redis.Redis('redis')
if(int(conn.llen("fib")) == 0):
    conn.rpush("fib", 2 ,1)

@app.route('/')
def index():
	Cont = zmq.Context()
	Sock = Cont.Sock(zmq.REQ)
	Sock.connect("tcp://worker:5555")
	x1 = conn.lindex("fib", 0)
	fib1 = int(x1)
	m = "Fibonacci num  = " + str(x1)
	Sock.send('1')
	curFib = Sock.recv()
	conn.lset("fib", 0, curFib)
	conn.lset("fib", 1, fib1)
	return m

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
