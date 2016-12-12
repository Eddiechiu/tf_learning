import threading, time
import Queue
import random

q = Queue.Queue()

def Producer(name):
	for i in range(20):
		q.put(i)
		print '+++++ Producer has made Item %s +++' % i
		time.sleep(random.randrange(3))

def Consumer(name):
	count = 0
	while count < 20:
		print '+++ Consumer has got Item %s +++' % q.get()
		count += 1
		time.sleep(random.randrange(2))

thread_p = threading.Thread(target=Producer, args=('Derong', ))
thread_c = threading.Thread(target=Consumer, args=('Eddie', ))

thread_p.start()
thread_c.start()