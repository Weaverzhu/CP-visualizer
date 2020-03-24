import os
import networkx as nx
import matplotlib.pyplot as plt

from treelayout import treeLayout

E_invalidInput = Exception("invalid input data")
E_inputfile = Exception("pls check ur input file path")

def wash(s):
    res = []
    n = len(s)
    for i in range(n):
        st = s[i].strip()
        if len(st) > 0:
            res.append(st)

    return res

class Config:
    def __init__(self):
        self.input_type = 0
        self.weighted = False
        self.directed = False
        self.isTree = False

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

        s = wash(f.readlines())
        for i in range(len(s)):
            s[i] = s[i].strip()

        self.u = []
        self.v = []
        self.w = []
        self.m = 0
        if 4 <= self.input_type <= 5:
            self.n = int(s[0])
            self.m = self.n - 1
            if self.input_type == 5:
                self.input_type = 3
                self.weighted = True
            else:
                self.weighted = False
                self.input_type = 1
            self.isTree = True
        if self.input_type == 0:
            self.n = len(s[0])
            for i in range(self.n):
                st = 0 if self.directed else i + 1
                for j in range(st, self.n):

                    if s[i][j] != '0':
                        self.u.append(i+1)
                        self.v.append(j+1)
            self.m = len(self.u)
        elif self.input_type == 1 or self.input_type == 3:
            if self.m == 0:
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
                a = list(map(int, s[i].split()))
                st = 0 if self.directed else i+1
                for j in range(st, self.n):
                    ux, vx, wx = i+1, j+1, a[j]
                    if wx > 0:
                        self.u.append(ux)
                        self.v.append(vx)
                        self.w.append(wx)
            self.m = len(self.u)
        elif self.input_type == 6:
            pass

    def go(self):
        G = nx.DiGraph() if self.directed else nx.Graph()
        G.add_nodes_from(range(1, self.n+1))
        for i in range(self.m):
            if not self.weighted:
                G.add_edge(self.u[i], self.v[i])
            else:
                G.add_edge(self.u[i], self.v[i], weight=self.w[i])
        # nx.draw_planar(G, with_labels=True)
        if not self.isTree:
            pos = nx.planar_layout(G)
        else:
            pos = treeLayout(G)
        
        if self.weighted:
            edge_labels = dict([((u, v,), d['weight'])
                                for u, v, d in G.edges(data=True)])
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, with_labels=True)
        plt.show()
