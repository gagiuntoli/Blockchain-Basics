import threading
import time
import random

def printA():
	print("A -> thread id: ", threading.get_native_id())
	time.sleep(4)

def printB():
	print("B -> thread id: ", threading.get_native_id())
	time.sleep(2)

def printAny(inlist):
	print("C -> thread id: ", threading.get_native_id())
	for i in inlist:
		print(i)
		time.sleep(1)

print("START -> thread id: ", threading.get_native_id())
t1 = threading.Thread(target=printA)
t2 = threading.Thread(target=printAny, args=(("ARG A", "ARG B", "ARG C"),))

t1.start()
t2.start()

printB()

t1.join()
t2.join()
print("END -> thread id: ", threading.get_native_id())
