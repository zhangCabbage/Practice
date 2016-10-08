#coding:utf-8

class Person(object):
    def __init__(self, name, age):
        self.name, self.age = name, age

    def __str__(self):
        # 我不知道这里为什么format中需要使用self=self?
        return "The guy is {self.name}, and is {self.age} old!".format(self=self)

print str(Person("zhang", 24))
