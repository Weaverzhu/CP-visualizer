#!/usr/bin/python3
import os
import networkx as nx
import matplotlib.pyplot as plt


E_invalidInput = Exception("invalid input data")
E_inputfile = Exception("pls check ur input file path")


class Config:
    def __init__(self):
        self.input_type = 0
        self.weighted = False
        self.directed = False

    def setInputType(self, input_type):
        self.input_type = input_type
        if self.input_type >= 2:
            self.weighted = True

    def setDirected(self, s):
        if s is None or s.strip().__len__() == 0:
            return
        if s[0] == 'y' or s[0] == 'Y':
            self.directed = True

    def readFromFile(self, path):
        f = open(path, "r")
        if not os.path.exists(path):
            raise E_inputfile

        s = f.readlines()
        for i in range(len(s)):
            s[i] = s[i].strip()

        self.u = []
        self.v = []
        self.w = []

        if self.input_type == 0:
            self.n = len(s[0])
            for i in range(self.n):
                st = 0 if self.directed else i + 1
                print(len(s[i]))
                for j in range(st, self.n):
                    print(i, j)
                    if s[i][j] != '0':
                        self.u.append(i)
                        self.v.append(j)
            self.m = len(self.u)
        elif self.input_type == 1 or self.input_type == 3:
            self.n, self.m = map(int, s[0].split())
            if self.m != len(s) - 1:
                raise E_invalidInput
            for i in range(1, len(s)):
                ux, vx, wx = 0, 0, 0
                if self.weighted:
                    ux, vx, wx = map(int, s[i].split())
                else:
                    ux, vx = map(int, s[i].split())
                self.u.append(ux)
                self.v.append(vx)
                self.w.append(wx)
            assert(self.m == len(self.u))
        elif self.input_type == 2:
            self.n = len(s)

            for i in range(self.n):
                a = map(int, s[i].split())
                st = 0 if self.directed else i+1
                for j in range(st, self.n):
                    ux, vx, wx = i, j, a[i][j]
                    if wx > 0:
                        self.u.append(ux)
                        self.v.append(vx)
                        self.w.append(wx)
            self.m = len(self.u)

    def go(self):
        G = nx.DiGraph() if self.directed else nx.Graph()
        G.add_nodes_from(range(self.n))
        for i in range(self.m):
            if not self.weighted:
                G.add_edge(self.u[i], self.v[i])
            else:
                G.add_edge(self.u[i], self.v[i], self.w[i])
        nx.draw_planar(G, with_labels=True)
        plt.show()


print('Greetings, choose an input type (default: 0)')
print('''
0(matrix):     1(edges):     2(number matrix):     3(edges with weight)
011            3 2           0 1 2                 3 2
101            1 2           1 0 2                 1 2 1
110            2 3           2 0 1                 2 3 2
3 1
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