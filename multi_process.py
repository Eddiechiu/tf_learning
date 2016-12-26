from multiprocessing import Pool
import os, time

def some_task(name):
	print('Task %s (%s) is running...' % (name, os.getpid()))
	start = time.time()
	time.sleep(2)
	end = time.time()
	print('Task %s runs for %0.2f seconds.' % (name, (end-start)))

print('Parent process %s' % os.getpid())
p = Pool()
for i in range(1):
	p.apply_async(some_task, args=(i,))
print('waiting for all subprocesses')
p.close()
p.join()
print('done')