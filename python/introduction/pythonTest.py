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

def iteratorTest():
    """
    关于__iter__ | next | __next__ 的关系？？
    可迭代对象（Iterable）：实现了 __iter__ 方法

    可迭代对象通过__iter__方法获得迭代器Iterator
    然后迭代器通过其__next__方法进行迭代，返回数值结果
    生成器也是迭代器，所以当在__iter__中通过yield返回时，不需要使用next

    iterator对象需要 __iter__ 和 next 两个函数，python3中换成 __next__
    以下实现方式参见：
    http://stackoverflow.com/questions/19151/build-a-basic-python-iterator
    """
    print("iterator Test -->")
    class Counter:
        def __init__(self):
            self.nums = (x for x in range(10))
            self.all_nums = []

        def __iter__(self):
            print "__iter__12"
            i = 0
            while True:
                if i < len(self):
                    yield self.all_nums[i]
                else:
                    yield next(self)
                i += 1

        def next(self): # Python 3: def __next__(self)
            print "next"
            return self.__next__()

        def __next__(self):
            print "__next__"
            try:
                num = next(self.nums)
                self.all_nums.append(num)
                return num
            except StopIteration:
                raise StopIteration('Counter contains no more nums.')

        def __len__(self):
            return len(self.all_nums)

    a = Counter()
    print list(a)
    print list(a)


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
    iteratorTest()
