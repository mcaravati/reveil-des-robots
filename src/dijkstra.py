from graph import Graph 
from cli import  read_file
import argparse

#Get indexes of "R"
def get_Drobot_position(Graph): 
    for i in range(0,Graph.N): 
        for j in range(0,Graph.N): 
            if (Graph.nodes[(i,j)].type == 'R'): 
                return (i,j)

#Get indexes of other Robots
def get_Robots_positions(Graph): 
    l = []
    for i in range(0,Graph.N):
        for j in range(0,Graph.N): 
            if (Graph.nodes[(i,j)].type != None and 
                Graph.nodes[(i,j)].type != 'X' and
                Graph.nodes[(i,j)].type != 'E' and
                Graph.nodes[(i,j)].type != 'R' ):

                l.append((i,j))

    return l

#Get the closest robot in terms of distance
def get_close_robot(Drobot ,robots):
    l = []
    for i in range(0,len(robots)):
        l.append((abs(Drobot[0] - robots[i][0])+(abs(Drobot[1] - robots[i][1]))))
    return robots[l.index(min(l))]

#modify trajet to get the minimum trajectory for "R" to wake other robots up, without taking in concideration their help
def reveil_robots(grid, Drobot, Orobots, grey, trajet):
    l = Orobots.copy() 
    if (len(l) == 0): 
        return trajet   
    closeRobot1 = get_close_robot(Drobot, l)
    l.remove(closeRobot1)
    if (closeRobot1 not in grey):        
        trajet.append(closeRobot1)
        grey.append(closeRobot1)
    reveil_robots(grid, closeRobot1, l, grey, trajet)
#
# This function modify 'trajet' to get movements for each robot (trajet is a dictionnary)
# Ex : trajet[0] for Robot "R" 
#
def Multiple_reveil_Robot(grid, Drobot, Orobots, trajet):
    trajet_Drobot = [Drobot]
    first_neighbors = [i for i in Orobots]
    i=0
    while(len(first_neighbors) >= 1):
        GREY=[]
        trajet[trajet_Drobot[0]] = []
        reveil_robots(grid, trajet_Drobot[0], first_neighbors, GREY, trajet_Drobot)
        if (len(trajet_Drobot)>2):
            for i in range (1,len(trajet_Drobot), (len(trajet_Drobot)+1)%2+1):
                (trajet[trajet_Drobot[0]]).append(trajet_Drobot[i])
        else : 
            (trajet[trajet_Drobot[0]]).append(trajet_Drobot[1])
        if (trajet[trajet_Drobot[0]] == []):
            break
        l = first_neighbors.copy()
        first_neighbors = []
        for i in range (0, len(l)):
            if(l[i] not in trajet[trajet_Drobot[0]]):
                first_neighbors.append(l[i])
        trajet_Drobot = [trajet[trajet_Drobot[0]][0]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str,
                        help='The path to the file to read.')
    parser.add_argument('N', type=int, help='The size of the grid.')
    args = parser.parse_args()
    grid = read_file(args.file_path, args.N)
    Drobot=get_Drobot_position(grid)
    Orobots=get_Robots_positions(grid)
    trajet, grey, Helpers=[Drobot], [], [Drobot]
    reveil_robots(grid, Drobot, Orobots, grey, trajet)
    print("movements considering only 'R' moving : ",Orobots)
    trajet1 = {}
    Orobots1 = get_Robots_positions(grid)
    values=[[] for i in range(0,len(Orobots1))]
    trajet1[Drobot]= []
    for i in Orobots1:
        for j in values:
            trajet1[i]=j
    grey1 = []
    Multiple_reveil_Robot(grid, Drobot, Orobots1, trajet1)
    print("movements for each robot: ", trajet1)
