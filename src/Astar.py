from graph import Graph, Node
from cli import read_file
import numpy as np
import matplotlib.pyplot as plt

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

def h(t : Node):
    def h_0(x : Node):
        return 0
    def h_euclidian(x : Node):
        return np.sqrt((t[0]-x[0])**2 + (t[1]-x[1])**2)
    def h_Manhattan(x : Node):
        return np.abs(t[0]-x[0]) + np.abs(t[1]-x[1])
    return [h_0, h_Manhattan, h_euclidian]

def extractDandhMin(GRIS,d,G,h):
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

def wayTo(parents, s, t):
    way = [t]
    i=1
    while way[0] != s :
        way.insert(0,parents[way[-i]])
        i+=1
    return way

def Astar(s : Node,t: Node ,G : Graph, hID : int): 
    d,parents = initialisation(s,G);
    GRIS = [s];
    NOIR = []
    while True :
        if len(GRIS)==0 :
            return (False,d,parent);
        x = extractDandhMin(GRIS,d,G,h(t)[hID]);
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

def wake_robots_alone(file_path, N, hID):
    G = read_file(file_path, N)
    Robots = get_Robots_positions(G)
    s = G.R
    Robots.sort(key=h(s)[hID])

    way = []
    while Robots != []:
        t = Robots.pop(0)
        way += wayTo(Astar(s,t,G,hID)[2],s,t)
        s = t
        Robots.sort(key=h(s)[hID])
    
    G.print_paths([way])
    plt.savefig(f"img/AstarAlone{hID}.png",dpi=300,bbox_inches="tight", pad_inches=0.1)

def wake_robots_with_help(file_path, N, hID):
    Paths = []
    def wake_robots_with_help_rec(r):
        if r==G.R or len(Robots) == 1:
            t = Robots.pop(0)
            Paths.append(wayTo(Astar(r,t,G,hID)[2],r,t))
            Robots.sort(key=h(r)[1])
            if r==G.R :
                wake_robots_with_help_rec(t)
        elif len(Robots) > 1:
            t1, t2 = Robots.pop(0), Robots.pop(0)

            Paths.append(wayTo(Astar(r,t1,G,hID)[2],r,t1))
            Paths.append(wayTo(Astar(r,t2,G,hID)[2],r,t2))
            Robots.sort(key=h(r)[1])

            wake_robots_with_help_rec(t1)
            wake_robots_with_help_rec(t2)

    G = read_file(file_path, N)
    Robots = get_Robots_positions(G)
    r = G.R
    Robots.sort(key=h(r)[1])
    wake_robots_with_help_rec(r)
    
    G.print_paths(Paths)
    plt.savefig(f"img/AstarWithOthers{hID}.png",dpi=300,bbox_inches="tight", pad_inches=0.1)

def measure():
    Distances=[]
    K=10
    d = []
    G = read_file(f"graph_{K}.txt", 1000)
    Robots = get_Robots_positions(G)
    s = G.R
    Robots.sort(key=h(s)[1])

    way = []
    while Robots != []:
        t = Robots.pop(0)
        way.append(wayTo(Astar(s,t,G,1)[2],s,t))
        s = t
        Robots.sort(key=h(s)[1])
    print(len(way))
    
if __name__ ==  "__main__" :
    wake_robots_alone("graph.txt",45,0)
    wake_robots_alone("graph.txt",45,1)
    wake_robots_alone("graph.txt",45,2)

    wake_robots_with_help("graph.txt",45,1)
    wake_robots_with_help("graph.txt",45,2)
