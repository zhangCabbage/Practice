#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading, time

#服务器端程序

def tcplink (sock, addr):
	print 'Accept new connection from %s:%s...' % addr
	sock.send('Welcome!')
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if data == 'exit' or not data:
			break
		sock.send('Hello, %s' % data)
	sock.close()
	print 'Connection from %s closed!' % data
		
def core_server ():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1',9998))
	s.listen(5)
	print 'waiting for connection....'
	while True:
		#接受一个新连接
		sock, addr = s.accept()
		#创建新线程处理TCP连接
		t = threading.Thread(target = tcplink, args = (sock, addr))
		t.start()
		
if __name__ =="__main__":
	core_server()