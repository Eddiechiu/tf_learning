from multiprocessing import Pool
import os, time

def some_task(name):
	print('Task %s (%s) is running...' % (name, os.getpid()))
	return name


if __name__=='__main__':
	a = []
	print('Parent process %s' % os.getpid())
	p = Pool()
	for i in range(9):
		a.append(p.apply_async(some_task, args=(i, )))
	print('waiting for all subprocesses')
	p.close()
	p.join()
	print([res.get() for res in a])