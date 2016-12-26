from multiprocessing import Pool
import os, time

def some_task(name):
	print('Task %s (%s) is running...' % (name, os.getpid()))
	start = time.time()
	time.sleep(2)
	end = time.time()
	print('Task %s runs for %0.2f seconds and it is now %s' % (name, (end-start), end))

if __name__=='__main__':	
	print('Parent process %s' % os.getpid())
	p = Pool()
	for i in range(9):
		p.apply_async(some_task, args=(i,))
	print('waiting for all subprocesses')
	p.close()
	p.join()
	print('done')