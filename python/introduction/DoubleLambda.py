#coding:utf-8

def pv(v) :
  print v

def test() :
  value = []
  value.append(0)
  value.append(1)
  x=[]
  for v in value :
    # x.append( ( lambda v: lambda: pv(v) )(v) ) # print 0 1
    x.append( lambda : pv(v) ) #print 1 1
    # x.append( ( lambda v : pv(v) )(v) ) #print 0 1, but need change xx() to xx
    # now this xx is a language : pv(v)
  return x

x = test()
for xx in x:
  xx()
print "---------------"

def line_conf():
    b = 15
    a = 2
    def line(x):
        return a*x+b
    return line       # return a function object

my_line = line_conf()
print(my_line.__closure__)
print(my_line.__closure__[0].cell_contents)
print(my_line.__closure__[1].cell_contents)
