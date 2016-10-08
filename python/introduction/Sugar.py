#coding:utf-8

count = 0

def sugar1(total, last, list, level):
    """ 方法1中递归暴力解法 """
    global count
    for num in xrange(last+1, total+1):
        list[level] = num
        list[level+1] = total-num
        if list[level+1] <= list[level]:
            break
        if level == 8: #control to stop
            count += 1
            continue
        sugar1(list[level+1], list[level], list, level+1)

def sugar2(total, last, level):
    """ 其实我们可以针对这种递归暴力解法进行优化 """
    if sum(xrange(last+1, last+1+10-level+1)) > total:
        return 0
    elif level == 10:
        return 1
    else:
        return sum(sugar2(total-x, x, level+1) for x in xrange(last+1, total+1))

n = 10
child = [0]*n
total = 100
sugar1(total, 0, child, 0)
print "方法1 --> ", count
print "方法2 --> ", sugar2(total, 0, 1)
