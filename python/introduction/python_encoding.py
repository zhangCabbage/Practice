#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import chardet

a = "张家桦"
print chardet.detect(a)
print a
b = u"高亚弘"
#print chardet.detect(b)
print "----"+b #不能输出Unicode
print b.encode("gbk")
print b.encode("gb2312")
print b.encode("utf-8")
#print b.encode("ascii")

#a_gbk_unicode = a.decode("gbk")
a_utf_unicode = a.decode("utf-8") #只能通过正确的方式解码成Unicode
#a_ascii_unicode = a.decode("ascii")
print a_utf_unicode.encode('utf-8')