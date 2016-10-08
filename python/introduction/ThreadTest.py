#!/usr/bin/python
# -*- coding:utf-8 -*-

import time, threading

def loop ():
	print "thread %s is running" % threading.current_thread().name
	n = 0
	while n<5:
		n = n+1
		print "---",n
		time.sleep(1)
	print "thread %s ended" % threading.current_thread().name

def test_thread ():
	print "thread %s is running" % threading.current_thread().name
	t = threading.Thread(target=loop,name="LoopThread")
	t.start()
	t.join()
	print "thread %s is ended" % threading.current_thread().name

if __name__ == "__main__":
	test_thread()
