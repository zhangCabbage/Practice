#coding:utf-8

import functools

def log(text):
    if callable(text):
        @functools.wraps(text)
        def wrapper(*args, **kw):
            print "{0} --> {1}".format("begin ", text.__name__)
            text(*args, **kw)
            print "{0} --> {1}".format("end ", text.__name__)
        return wrapper
    else:
        print "this param is --> ", text
        def decor(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                print "{0} --> {1}".format("begin ", func.__name__)
                func(*args, **kw)
                print "{0} --> {1}".format("end ", func.__name__)
            return wrapper
        return decor

@log("LOG")
def decorator1():
    print "Hello World, one!"

@log
def decorator2():
    print "Hello World, two!"

decorator1()
print
decorator2()
