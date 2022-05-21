from graph import Graph, Node
from cli import read_file

def initialisation(s : Node,G : Graph):
    d,parents = {},{}
    for i in range(G.N):
        for j in range(G.N):
            if G.nodes[(i,j)].type != 'X' :
                d[(i, j)] = float("inf")
                parents[(i, j)] = 0
    d[s] = 0
    return d, parents

def index(y, tab):
    for i in range(len(tab)):
        if tab[i] == y:
            return i
    return -1

def colorGRIS(y, GRIS, NOIR):
    if y in NOIR:
        NOIR.pop(index(y,NOIR))
        GRIS.append(y)
    elif not(y in GRIS):
        GRIS.append(y)
    return GRIS, NOIR

def colorNOIR(y, GRIS, NOIR):
    if y in GRIS:
        GRIS.pop(index(y,GRIS))
        NOIR.append(y)
    elif not(y in NOIR):
        NOIR.append(y)
    return GRIS, NOIR

def h(x):
    return 0
def extractDandhMin(GRIS,d,G):
    dmin = float("inf")
    xmin = GRIS[0]
    for x in GRIS :
        if d[x] + h(x) < dmin :
            dmin = d[x] + h(x)
            xmin = x
    return xmin

def releaseAstar(e,G,d,parent,GRIS,NOIR):
    (x,y) = e
    if d[x]+1 < d[y]:
        d[y] = d[x] + 1
        parent[y] = x ; 
        GRIS, NOIR = colorGRIS(y,GRIS,NOIR)
    return d, parent, GRIS, NOIR

def wayTo(parents,s,t):
    way = [t]
    i=1
    while way[0] != s :
        way.insert(0,parents[way[-i]])
        i+=1
    return way

def Astar(s : Node,t: Node ,G : Graph): 
    d,parents = initialisation(s,G);
    GRIS = [s];
    NOIR = []
    while True :
        if len(GRIS)==0 :
            return (False,d,parents);
        x = extractDandhMin(GRIS,d,G);
        if x==t:
            return (True,d,parents)
        L = G.get_neighbors(x)
        filter(lambda x : x.type != 'X', L)
        for i in range(0,len(L)) :
            if (G.nodes[L[i]].type != 'X'):
                d, parents, GRIS, NOIR = releaseAstar((x,L[i]),G,d,parents,GRIS,NOIR);
        GRIS, NOIR = colorNOIR(x, GRIS, NOIR)

def get_Robots_positions(G): 
    l = []
    for i in range(0,G.N):
        for j in range(0,G.N): 
            if (G.nodes[(i,j)].type != None and 
                G.nodes[(i,j)].type != 'X' and
                G.nodes[(i,j)].type != 'E' and
                G.nodes[(i,j)].type != 'R' ):

                l.append((i,j))
    return l

def get_close_robot(Drobot ,robots):
    l = []
    for i in range(0,len(robots)):
        l.append((abs(Drobot[0] - robots[i][0])+(abs(Drobot[1] - robots[i][1]))))
    return robots[l.index(min(l))]

def wake_robots(file_path, N):
    G = read_file(file_path, N)
    G.generate_random_obstacles(5)
    Robots = get_Robots_positions(G)
    s = G.R
    way = []
    for t in Robots :
        way += wayTo(Astar(s,t,G)[2],s,t)
        s = t
    G.print_path(way)

if __name__ ==  "__main__" :
    wake_robots('graph.txt', 60)