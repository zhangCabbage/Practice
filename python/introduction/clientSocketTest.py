#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
#客户端程序
def core_client ():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 9998))
	print s.recv(1024)
	for data in ['Michael', 'Tracy', 'Sarah']:
		s.send(data)
		print s.recv(1024)
	s.send('exit')
	s.close()

if __name__ =="__main__":
	core_client()