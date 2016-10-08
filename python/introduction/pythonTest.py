#coding:utf-8

# from collections import Iterable
import re
import chardet
import os

def myGenerator():
    for char in "zh":
        yield char
    for i in range(2):
        yield i

def generatorTest():
    for i in range(4):
        print myGenerator().next(), #
        # 上面的相当于每次都是一个新的myGenerator()可迭代函数对象的next方法
        # 所以这种形式每次都返回第一个
    print ""
    a = myGenerator();
    for i in range(4):
        print a.next(),
    print ""

def listTest(myList, myValue):
    """ 引用传递参数 """
    mylist[0:0] = [-1, 0]
    myValue = 1000

def loopTest(m, n):
    """ 可以多层嵌套使用_ """
    print ""
    for _ in xrange(m):
        for _ in xrange(n):
            print "Z",
        print ""

def christmasTree(hight):
    l = range(hight)
    l.reverse()
    for i in l:
        print "%s%s"%(" "*i, "*"*((hight-i-1)*2+1))

def en_decodeTest():
    print chardet.detect("zhang")

def filePathTest():
    """ 关于文件路径问题 """
    print __file__
    print os.path.dirname(__file__)
    print os.path.dirname(os.path.dirname(__file__))

if __name__ == '__main__':
    print "Hello World!"
    generatorTest()

    mylist = [1, 2, 3, 4]
    myValue = 5
    print mylist, myValue
    listTest(mylist, myValue);
    print mylist, myValue

    christmasTree(5)
    en_decodeTest()

    print "-----------"
    for _ in xrange(5):
        print "H",

    loopTest(2, 4)
    filePathTest()
