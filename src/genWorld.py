import random

def genWorld(N : int, nrobots : int):
    X = [0 for i in range(N)]
    Y = [0 for i in range(N)]
    R = [0,0]
    R[0] = random.randint(0,N-1)
    R[1] = random.randint(0,N-1)
    X[R[0]] = 1
    Y[R[1]] = 1
    with open(f"graph_{nrobots}.txt", 'w') as f:
        f.writelines(f"R : ({R[0]},{R[1]})\n")
        for n in range(1,nrobots+1):
            robot = [0,0]
            robot[0] = random.randint(0,N-1)
            robot[1] = random.randint(0,N-1)

            while robot==R and X[robot[0]]==1 and Y[robot[1]]==0:
                robot[0] = random.randint(0,N-1)
                robot[1] = random.randint(0,N-1)
                
            X[robot[0]] = 1
            Y[robot[1]] = 1
            f.writelines(f"{n} : ({robot[0]},{robot[1]})\n")
    
if __name__ == "__main__":
    for K in [10,50,200,1000]:
        genWorld(1000, K)