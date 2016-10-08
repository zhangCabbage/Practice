#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from multiprocessing import Pool
import os, time, random

# 子进程要执行的代码
def run_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

def test_process ():
	print 'Parent process %s.' % os.getpid()
	p = Process(target=run_proc, args=('test',))
	print 'Process will start.'
	p.start()
	p.join()
	print os.getpid()
	print 'Process end.'

def long_time_task(name):
	print 'Run task %s (%s)...' % (name, os.getpid())
	start = time.time()
	time.sleep(random.random() * 3)
	end = time.time()
	print 'Task %s runs %0.2f seconds.' % (name, (end - start))

def test_pool ():
	print 'Parent process %s.' % os.getpid()
	p = Pool(3)
	for i in range(5):
		p.apply_async(long_time_task, args=(i,))
	print 'Waiting for all subprocesses done...'
	p.close()
	p.join()
	print 'All subprocesses done.'

if __name__=='__main__':
	test_pool()