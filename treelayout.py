import networkx as nx
x = []
y = []
adj = []
f = []
def dfs(u, la):
    global adj, f, y, x
    f[u] = la
    y[u] = y[la] + 1
    sz = len(adj[u])
    for v in adj[u]:
        if v == la:
            sz -= 1
    
    offset = (sz - 1) / 2
    j = 0
    for v in adj[u]:
        if v == la:
            continue
        x[v] = x[u] - offset + j
        j += 1
        dfs(v, u)
    
def treeLayout(G : nx.Graph()):
    global x, y, adj, f
    n = len(G.nodes())
    root = 1
    adj = [[] for i in range(n + 1)]
    x = [0 for i in range(n + 1)]
    y = [0 for i in range(n + 1)]
    f = [0 for i in range(n + 1)]
    
    for ed in G.edges():
        adj[ed[0]].append(ed[1])
        adj[ed[1]].append(ed[0])
    dfs(1, 1)
    xy = [[0, 0] for i in range(n + 1)]
    xstep = 4 / (max(x) - min(x)) if max(x) != min(x) else 1
    ystep = 4 / (max(y) - min(y)) if max(y) != min(y) else 1
    for i in range(1, n + 1):
        xy[i][0] = x[i] * xstep
        xy[i][1] = -y[i] * ystep
    # print(xy)
    return {k: xy[k] for k in G.nodes.keys()}

