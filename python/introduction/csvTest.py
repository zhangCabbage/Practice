#!/usr/bin/python
#coding:utf-8

import csv

def csvRead(filepath, dialect="excel"):
    with open(filepath, "rb") as file:
        lines = csv.reader(file, dialect)
        for line in lines:
            print line

def csvWrite(filepath):
    with open(filepath, "wb") as file:
        writeHandle = csv.writer(file)
        writeHandle.writerow([10, 'abc'])
        writeHandle.writerow([11, 'def'])
        writeHandle.writerows([[12,'ghi'], [13, 'jjj']])

def customDialect():
    """ 注册使用自定义的dialect """
    csv.register_dialect("lineDialect", delimiter="|", quoting=csv.QUOTE_ALL)

if __name__ == '__main__':
    csvRead("test.csv")
    # print "-------after--------"
    # customDialect()
    # csvRead("test.csv", "lineDialect")
    # csvWrite("test.csv")
