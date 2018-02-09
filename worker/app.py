import redis
import zmq 

def Fibbonachi(DataBaseConn):
    pipe = DataBaseConn.pipeline()
    while 1:
            try:
                print('TRYING')
                pipe.watch("fibonacciNumber")
                fibNum1 = int(pipe.lindex("fibonacciNumber", 1))
                fibNum2 = int(pipe.lindex("fibonacciNumber", 0))
                sumFib = fibNum1 + fibNum2
                pipe.lset("fibonacciNumber", 0, sumFib)
                pipe.lset("fibonacciNumber", 1, fibNum2)
                pipe.execute()
                break
            except redis.WatchError:
				print('can't calculate')
                continue
            finally:
                pipe.reset()
    return
		
print('BIND')
Cont = zmq.Context()
socket = Cont.socket(zmq.REP)
socket.bind("tcp://*:5555")

DataBaseConn = redis.Redis('redis')
print('BINDED')
while True:
	poke = socket.recv()
        print('RECEIVED POKE FROM MASTER')
	Fibbonachi(DataBaseConn)
	print('METHOD Fibbonachi executed')
	socket.send('New Fibonacci number calculated')
print ('SENT ENDMESSAGE')
