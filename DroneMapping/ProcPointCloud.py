from progressBar import ProgressBar
from missingDataSolved import findAllMissing
import os


def main():
    ACCURACY = 1            #controls the accuracy when solving for missing data points
                            #1 = high accuracy 
                            #0 = standard accuracy    
    longs = set()       #unique longitudes
    latMin = None       #minimum latitudes
    longMin = None      #minimum longitude
    latMax = None       #maximum latitude
    longMax = None      #maximum longitude
    altMax = None       #maximum altitude
    x = 0               #current line number
    size = 0
    interval = float(input("Enter the inches per pixel: "))
    fileName = input("Enter file name: ")
    fileName = "./Drone Data/" + fileName      
    
    size = getFileSize(fileName)
    
    pbar = ProgressBar(size,"Reading in data...")  
    
    #reads in the data from the file
    file = open(fileName)
    for line in file:   
        points = []
        vals = line.rstrip().split(',')
        #for element in vals:
            #temp = element.split(' ')
            #points.append(temp[len(temp)-1])
        #vals = points        
        longs.add(round(float(vals[1]),2))       #places unique longs in a set          
        
        #determines the max and min latitudes
        if latMax == None:
            latMax = abs(round(float(vals[0]),2))
            latMin = abs(round(float(vals[0]),2))
        elif abs(round(float(vals[0]),2)) > latMax:
            latMax = abs(round(float(vals[0]),2))
        elif abs(round(float(vals[0]),2)) < latMin:
            latMin = abs(round(float(vals[0]),2))        
        
        #determines the max and min longitudes
        if longMax == None:
            longMax = abs(round(float(vals[1]),2))
            longMin = abs(round(float(vals[1]),2))
        elif abs(round(float(vals[1]),2)) > longMax:
            longMax = abs(round(float(vals[1]),2))
        elif abs(round(float(vals[1]),2)) < longMin:
            longMin = abs(round(float(vals[1]),2))
            
        #determine the max altitude
        if altMax == None:
            altMax = abs(float(vals[2]))
        elif abs(float(vals[2])) > altMax:
            altMax = abs(float(vals[2]))
            
        pbar.update()       #updates the prgress bar
    file.close()            #closes the file 
    
    file = open(fileName)
    interval = 5 - int(1/interval)  
    if interval == 0:
        interval = 1
    matrix = makeMatrix(int(((round((float(latMax)-float(latMin)),2) * 100))/interval)+1,int(((round((float(longMax)-float(longMin)),2) * 100))/interval)+1)
    pbar = ProgressBar(size,"Filling matrix...")
    count = 0
    num = 0
    
    for line in file:
        points = []
        vals = line.rstrip().split(',')
        #for element in vals:
            #temp = element.split(' ')
            #points.append(temp[len(temp)-1])
        #vals = points
        x = int((round((abs(float(vals[0])) - float(latMin)),2) * 100))
        y = int((round((abs(float(vals[1])) - float(longMin)),2) * 100))
        try:
            matrix[int(x/interval)][int(y/interval)] = altMax - abs(float(vals[2]))
            num += 1
        except:
            count = count + 1
            
        pbar.update()
    file.close()
    
    matrix = findAllMissing(matrix,ACCURACY)    
    writeBack(matrix)
    
    print()
    print("Number missed...................= ",count)
    print("Number added....................= ",num)
    print("Number of alts..................= ",size)
    print("Size of the matrix..............= ",(len(matrix) * len(matrix[0])))
    print("Matrix height...................= ",len(matrix) - 1)
    print("Matrix width....................= ",len(matrix[0]) - 1)    
    print("Difference in latitude..........= ",int(round((float(latMax)-float(latMin)),2) * 100))
    print("Difference in longitude.........= ",int(round(float((longMax)-float(longMin)),2) * 100))    
    print("Average dist between points.....= ", interval," cm(s)") 
    print("Average number of Longs per alt.= ",round(size/len(longs),2))
    print(latMin,"--->",latMax)
    print(longMin,"--->",longMax)    
    
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

#creates an empty matrix
def makeMatrix(y,x):
    rowArray = []
    matrix = []
    i = 0
    j = 0
    pbar = ProgressBar(y,"Creating Matrix...")
    
    #creates the appropriately sized rowArray
    while i < y:
        j = 0
        rowArray = []
        while j < x:
            rowArray.append(None)
            j = j + 1
        matrix.append(rowArray)
        i = i + 1
        pbar.update()
    return matrix

#write the data to three text files
#1. latitudes
#2. longitudes
#3. the matrix
def writeBack(matrix):
    size = len(matrix) + len(matrix[0]) + int((len(matrix) * len(matrix[0])))
    pbar = ProgressBar(size,"Writing points to file...")    #initializes the progress bar
    line = ""
    i = 0
    
    #gets the appropriate file name
    it = str(getIteration())
    newFile = "./3D Maps/3D Latitudes(" + it + ").txt"
    
    #opens the file
    file = open(newFile,"w+") 
    
    #writes the latitudes to the text file
    while i < len(matrix):
        if i < len(matrix) - 1:
            line = line + str(i) + ","
        else:
            line = line + str(i) + "\n"
        pbar.update()
        i = i + 1
    file.write(line)
    file.close
    
    newFile = "./3D Maps/3D Longitudes(" + it + ").txt"
    
    #opens the file
    file = open(newFile,"w+")
    
    line = ""           #resets line
    i = 0           #resets count
    #writes the longitudes to the text file
    while i < len(matrix[0]):
        if i < len(matrix[0]) - 1:
            line = line + str(i) + ","
        else:
            line = line + str(i) + "\n"
        pbar.update()
        i = i + 1
    file.write(line)
    file.close
    
    newFile = "./3D Maps/3D Matrix(" + it + ").txt"
    i = 0
    
    #opens the file
    file = open(newFile,"w+")    
    
    #writes the matrix to the textfile
    for row in matrix:
        line = ""           #resets line
        count = 0           #resets count    
        for element in row:
            if count < len(matrix[0]) - 1:
                line = line + str(element) + ","
            else:
                line = line + str(element) + '\n'
            pbar.update()
            count = count + 1
        file.write(line)        
    
    file.close()
    temp = "Done. 3D Map("+it+") has been created. You may now close the program."
    print(temp)
    return    

#gets the iteration of 3D model points generated and updates the iteration count
def getIteration():
    filePath = "./3D Maps/Iteration.txt"
    iteration = 0
    
    #checks if the file exists and if it does opens it
    if os.path.isfile(filePath):
        file = open(filePath, "r")
        iteration = int(file.readline())
        iteration = iteration + 1
        file.close()
        
    #if the file doesnt exist it is created and zero is written in it
    file = open(filePath, "w+")
    file.write(str(iteration))
    
    file.write("\n")
    file.close()
    return iteration

main()