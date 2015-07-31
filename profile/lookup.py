# f() and g() iterates over the keys of a dict in two different ways.

import sys

def f(d):
    for k in d:
        pass

def f1(d):
    for k in d.keys():
        pass

def g(d, n):
    if n in d:
        pass

def g1(d, n):
    if n in d.keys():
        pass

def h(l, n):
    if n in l:
        pass

def main(argv):
    n = 5
    if len(argv) > 1:
        n = int(argv[1])
    d = {i:i for i in range(n)}
    l = [i for i in range(n)]
    f(d)
    f1(d)
    g(d, n)
    g1(d, n)
    h(l, n)
    
if __name__ == "__main__":
    main(sys.argv)
