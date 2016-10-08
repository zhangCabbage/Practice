#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
def search (x, find_string):
	#
	for i in os.listdir(x):
		if os.path.isdir(os.path.join(x, i)):
			search(os.path.join(x, i), find_string)
		elif os.path.isfile(os.path.join(x, i)) and (find_string in i):
			print os.path.join(x, i)
			
def test_search ():
	#
	if len(sys.argv)!=2:
		print "参数"
	else:
		s = '.'
		search(s, sys.argv[1])
		return 1

def writeToFile ():
	with open('C:\\Users\\BFD_466\\Desktop\\123\\test.txt', 'w') as f:
		f.write("zhang jiahua 巴巴变")
		f.write("阿打发阿")
		# ����д�룬�����Զ���ӻ���
		# w�ڶ���д�Ḳ��ԭ�������ļ�����������


if __name__ == "__main__":
	#test_search()
	#writeToFile() 
	a = os.listdir('C:\Users\BFD_466\Desktop')
	print a
	print type(a)
	print type(a[7])
	print a[7]
	#print a[7].encode("gbk2312")
	b = 'zhang\\jia\\hua'
	print b
	t = u''
	print t
	#print b.split('\\\\')
	
