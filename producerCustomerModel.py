import threading, time
import Queue
import random

q1 = Queue.Queue()
q2 = Queue.Queue()

def ProducerA():
	for i in range(10):
		q1.put(i)
		print '*** A has made Item %s ***' % i
		time.sleep(random.randrange(2))

def ProducerB():
	count = 0
	while count < 10:
		i = q1.get()
		print '+++ B get Item %s from A and complete Item %s +++' % (i, i)
		q2.put(i)
		count += 1
		time.sleep(random.randrange(2))


def Consumer():
	count = 0
	while count < 10:
		print '--- Consumer has got Item %s ---' % q2.get()
		count += 1
		time.sleep(random.randrange(3))

thread_p1 = threading.Thread(target=ProducerA)
thread_p2 = threading.Thread(target=ProducerB)
thread_c = threading.Thread(target=Consumer)

thread_p1.start()
thread_p2.start()
thread_c.start()