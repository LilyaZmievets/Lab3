import redis
import zmq 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def Fibbonachi():
	Conn = redis.Redis('redis')
	x2 = Conn.lindex("fib", 1)
	x1 = Conn.lindex("fib", 0)
	f1 = int(x1)
	f2 = int(x2)
	curFib = f1 + f2
	strCurFib = str(curFib)
	return strCurFib

while True:
	mes = socket.recv()
	curFib = Fibbonachi()
	socket.send(curFib)
