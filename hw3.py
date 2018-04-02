import random
 


def zipmaze(horizontal, vertical):
    s = ""
    horizontal[20][20] = " "
    horizontal[20][19] = " "
    horizontal[0][0] = "  "

    for(h,v) in zip(horizontal, vertical):
        temp = ""
        s+= temp.join(h)
        s+= "\n"
        s+= temp.join(v)
        s+= "\n"
    print(s); 


def make_maze(width = 20, height = 20):


    mazeModel =[] # mazemodel for dfs 
    for x in range(0,height):
        mazeModel.append([0]*(width))
        mazeModel[x].append(1)
    mazeModel.append([1]*(width+1))

    vertical =[] # vertical barrier representation
    for x in range(0,height):
        vertical.append(["| "]*(width+1))
    vertical.append([])

    horizontal =[] #horizontal barrier representation 
    for x in range(0,height+1):
        horizontal.append(["._"]*(width))
        horizontal[x].append('.')
    horizontal.append([])


    def dfs(x, y):
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        mazeModel[y][x] = 1

        for (a, b) in d:
            if not mazeModel[b][a]: 
                if a == x: 
                    horizontal[max(y, b)][x] = ". "
                if b == y: 
                    vertical[y][max(x, a)] = "  "
                dfs(a, b)
 
    dfs(width-1, height-1)
    zipmaze(horizontal,vertical)
 

make_maze()