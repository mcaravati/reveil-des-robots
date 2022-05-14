
from fileinput import close
from pydoc import Helper
from graph import Graph 
from cli import  read_file
import argparse

#Get indexes of "R"
def get_Drobot_position(Graph): 
    for i in range(0,Graph.N): 
        for j in range(0,Graph.N): 
            if (Graph.nodes[(i,j)].type != None): 
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
    if (len(Orobots) == 0): 
        return trajet   
    closeRobot1 = get_close_robot(Drobot, Orobots)
    Orobots.remove(closeRobot1)
    if (closeRobot1 not in grey):        
        trajet.append(closeRobot1)
        grey.append(closeRobot1)
    reveil_robots(grid, closeRobot1, Orobots, grey, trajet)
#
# This function modify 'trajet' to get movements for each robot 
# Ex : trajet[0] for Robot "R" 
#
def Multiple_reveil_Robot(grid, Drobot, Orobots, GREY, Helpers, trajet, index): # helpers should be initialized with Drobot
    if (len(Orobots) == 0): 
        return trajet
    closeRobot1 = get_close_robot(Drobot, Orobots)
    Orobots.remove(closeRobot1)
    Helpers.append(closeRobot1)
    list=[closeRobot1]
    if (closeRobot1 not in GREY):        
        trajet[index].append(closeRobot1)
        GREY.append(closeRobot1)
    for i in range(0, len(Helpers)):
        print(i) 
        helper_i = Helpers[i]
        Multiple_reveil_Robot(grid, helper_i, Orobots, GREY, Helpers, trajet, i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str,
                        help='The path to the file to read.')
    parser.add_argument('N', type=int, help='The size of the grid.')
    args = parser.parse_args()
    grid = read_file(args.file_path, args.N)
    Drobot=get_Drobot_position(grid)
    Orobots=get_Robots_positions(grid)
    trajet, grey, Helpers=[], [], [Drobot]
    reveil_robots(grid, Drobot, Orobots, grey, trajet)
    print(trajet)
    #Multiple_reveil_Robot(grid, Drobot, Orobots, grey,Helpers, trajet, index=0)
    #print(trajet)
