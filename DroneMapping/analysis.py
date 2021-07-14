from progressBar import ProgressBar
from findCorners import findAllCorners
import os

def main():
    ALTS = ["45 feet ", "60 feet ","75 feet ","90 feet ","105 feet"]
    
    userIn = options()        #gets user input to decide what is done
    print()
    print()
    print()
    if userIn == 1 or userIn == 4:         #displays analysis of one matrices
        it = int(input("Enter file iteration: "))
        
        if it == 0:
            sIt = 5
        else:
            sIt = it - 1
    
        baseCorners = baseRead()            #reads in the corners (baseline)
        perErr,viable,corners,avg = perError(it,baseCorners)
             
        line = "./3D Maps/3D Matrix("+str(it)+").txt"
        line2 = "./Drone Data/sample("+str(sIt)+").xyz"
        
        print("The percentage error for corner one...........= %5.2f"%round(perErr[0],2),"%           Viable: ",viable[0],"                 Altitude: ",corners[0])
        print("The percentage error for corner two...........= %5.2f"%round(perErr[1],2),"%           Viable: ",viable[1],"                 Altitude: ",corners[1])
        print("The percentage error for corner three.........= %5.2f"%round(perErr[2],2),"%           Viable: ",viable[2],"                 Altitude: ",corners[2])
        print("The percentage error for corner four..........= %5.2f"%round(perErr[3],2),"%           Viable: ",viable[3],"                 Altitude: ",corners[3])
        print("The average percentage error for iteration  "+str(it)+".= %5.2f"%round(avg,2),"%           Viable: ",viable[4],"         Average Altitude: ",round((corners[0]+corners[1]+corners[2]+corners[3])/4,3))
        print("The size of iteration "+str(it)+".......................= ",getSize(line),"mb")
        print("The size of point cloud file "+str(sIt)+"................= ",getSize(line2),"mb")
        print("Total size reduction..........................= ",round(abs((getSize(line)/getSize(line2) * 100) - 100),2), "%")
        print()
        print()
        
    elif userIn == 2 or userIn == 5:           #displays analysis of all matrices
        lower = 0
        higher = 4
        pci = 0                #point cloud iteration
        sIt = 5
        perErr = []
        viable = []
        corners = []
        avg = []
        
        while lower <= higher:
            baseCorners = baseRead()            #reads in the corners (baseline)
            pE,vi,cor,tot = perError(lower,baseCorners)
            perErr.append(pE)
            viable.append(vi)
            corners.append(cor)
            avg.append(tot)
            lower = lower + 1
            
        lower = 0
        print()
        while lower <= higher:
            line = "./3D Maps/3D Matrix("+str(lower)+").txt"
            line2 = "./Drone Data/sample("+str(sIt)+").xyz"
            
            print()
            print()
            print("The percentage error for corner one...........= %5.2f"%round(perErr[lower][0],2),"%           Viable: ",viable[lower][0],"                 Altitude: ",corners[lower][0])
            print("The percentage error for corner two...........= %5.2f"%round(perErr[lower][1],2),"%           Viable: ",viable[lower][1],"                 Altitude: ",corners[lower][1])
            print("The percentage error for corner three.........= %5.2f"%round(perErr[lower][2],2),"%           Viable: ",viable[lower][2],"                 Altitude: ",corners[lower][2])
            print("The percentage error for corner four..........= %5.2f"%round(perErr[lower][3],2),"%           Viable: ",viable[lower][3],"                 Altitude: ",corners[lower][3])
            print("The average percentage error for iteration  "+str(lower)+".= %5.2f"%round(100*avg[lower],2),"%           Viable: ",viable[lower][4],"         Average Altitude: ",round((corners[lower][0]+corners[lower][1]+corners[lower][2]+corners[lower][3])/4,3))
            print("The size of iteration "+str(lower)+".......................= ",getSize(line),"mb")
            print("The size of point cloud file "+str(sIt)+"................= ",getSize(line2),"mb")
            print("Total size reduction..........................= ",round(abs((getSize(line)/getSize(line2) * 100) - 100),2), "%")
            print()
            print()
            
            pci = pci + 1
            sIt = pci - 1
            lower = lower + 1
    
    #To determine the best choice accurancy and file sile are taken into consideration
    #accuracy is deemed more important than file size
    if userIn == 3 or userIn == 4 or userIn == 5:           #determines the best one to use
        points = []         #keeps track of each files points
        
        lower = 0
        higher = 4
        pci = 0                #point cloud iteration
        sIt = 5
        perErr = []
        total = []
        sizes = []
        
        i = 0
        #adds the correct number of elements to points
        while i <= higher:
            points.append(0)
            i = i + 1
        
        while lower <= higher:
            baseCorners = baseRead()            #reads in the corners (baseline)
            pE,vi,cor,tot = perError(lower,baseCorners)
            perErr.append(pE)
            total.append(tot)
            lower = lower + 1
        
        #determines the best altitude to use based on accuracy
        pointLeft = higher
        predPE = 5
        predAVG = 5

        for i in total:     #points for average accuracy
            low = 9999
            for element in total:
                if element < low:
                    low = element    
            points[total.index(low)] = points[total.index(low)] + pointLeft
            pointLeft = pointLeft - 1 
            total[total.index(low)] = 9999
            
        for i in range (len(perErr[0])):       #points for individual corner accuracy
            pointLeft = higher
            for j in range(len(perErr[0])):
                low = 9999
                for k in range(len(perErr)):
                    if perErr[k][i] < low:
                        low = perErr[k][i]
                        loc = k
                if low <= 5:
                    points[loc] = points[loc] + pointLeft
                    pointLeft = pointLeft - 1 
                    perErr[loc][i] = 9999  
        
        #determines the best altitude to used based on file size    
        lower = 0
        pointLeft = higher
        while lower <= higher:      #gets the file sizes
            line = "./3D Maps/3D Matrix("+str(lower)+").txt"
            sizes.append(getSize(line))
            lower = lower + 1
    
        for i in sizes:         #points for file size
            low = 9999
            for element in sizes:
                if element < low:
                    low = element    
            points[sizes.index(low)] = points[sizes.index(low)] + (pointLeft* (2/3))
            pointLeft = pointLeft - 1 
            sizes[sizes.index(low)] = 9999
        
        #prints the top three
        top = []
        for i in range(len(points)):        #finds the top 3 values
            low = 0
            for j in range(len(points)):
                if points[j] > low:
                    low = points[j]
                    point = low,j
            top.append(point)
            points[point[1]] = 0
            if len(top) == 3:
                break
        
        print("The best altitude for data collection.................= ",ALTS[top[0][1]],"        It scored %2.2f"%top[0][0],"out of 22.66")
        print("The second best altitude for data collection..........= ",ALTS[top[1][1]],"        It scored %2.2f"%top[1][0],"out of 22.66")
        print("The third best altitude for data collection...........= ",ALTS[top[2][1]],"        It scored %2.2f"%top[2][0],"out of 22.66")
        
    a = input("**Hit ENTER to close**")         #keeps the terminal open
    return
        
            
#gets the number of line in the file
def getFileSize(file):
    print("Getting file size...")
    inFile = open(file)
    x = 0
    for line in inFile:
        x = x + 1
    inFile.close()
    return x

#reads the file into a matrix
def readFile(it):
    temp = []
    matrix = []
    fileT = "./3D Maps/3D Matrix("+str(it)+").txt"
    size = getFileSize(fileT)
    heading = "Reading in matrix("+str(it)+")..." 
    pbar = ProgressBar(size,heading)    
    
    #reads in the data from the file
    file = open(fileT)
    for line in file:  
        temp = []
        vals = line.rstrip().split(',')
        for element in vals: 
            temp.append(float(element))
        matrix.append(temp)
        pbar.update()
    return matrix

#reads in the data for the baseline
'''      c1                c3
         -------------------
         |                 |
         |                 |
         -------------------
         c2                c4
'''
def baseRead():
    path = "./Analysis/Baseline.txt"
    corners = []
    
    file = open(path)
    for line in file:
        corners.append(float(line.rstrip()))
    
    return corners
        
#gets the file size of a file in mb
def getSize(name):
    return os.path.getsize(name) >> 20

#determines the percentage error for a matrix
def perError(it,baseCorners):
    matrix = readFile(it)               #reads in the matrix
    corners = findAllCorners(matrix)    #finds all the corners (processed data)
    
    #calculates percentage error and determines of it is a viable solution or not (percentage error <= 5%)
    perErr = []
    viable = []
    total = 0
    i = 0
    for e in corners:
        perErr.append(abs(e-baseCorners[i])/baseCorners[i] * 100)
        total += abs(e-baseCorners[i])/baseCorners[i]
        if perErr[i] <= 5:
            viable.append("True ")
        else:
            viable.append("False")
        i = i + 1
            
    if total/4 < .05:     
        viable.append("True ")
    else:
        viable.append("False")   
    
    return perErr,viable,corners,total/4

#displays the options menu
def options():
    print("-------------------------------------------------------")
    print("Choose one of the following options from below:")
    print("1.       Get analysis for one set of data.")
    print("2.       Get analysis for all sets of data.")
    print("3.       Determine the best altitude to record data.")
    print("4.       Option 1 and Option 3.")
    print("5.       Option 2 and Option 3.")
    print("-------------------------------------------------------")
    return int(input("Response: "))
    
main()