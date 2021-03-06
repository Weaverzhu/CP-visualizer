#!/usr/bin/python3
import os
import networkx as nx
import matplotlib.pyplot as plt

from config import Config

print('Greetings, choose an input type (default: 0)')
print('''
0(matrix):     1(edges):     2(number matrix):     3(edges with weight)
011            3 2           0 1 2                 3 2
101            1 2           1 0 2                 1 2 1
110            2 3           2 0 1                 2 3 2

4(tree):       5(tree w):    6(tree with f):
3              3             3
1 2            1 2 1         0 1 2
2 3            2 3 2
''')
c = Config()
i = input()
if len(i.strip()) == 0:
    i = 0
else:
    i = int(i)
c.setInputType(i)

print('''
Is the graph directed? (default: no) [y/n]
''')

c.setDirected(input())
print('''
Where is the input file? (default: ./in.txt)
''')
p = "./in.txt"
i = input()
p = i if len(i.strip()) > 0 else p

c.readFromFile(p)
c.go()
