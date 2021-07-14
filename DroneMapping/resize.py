from progressBar import ProgressBar
import os

def main():
    user = dispMenu()
    if user == 2:
        it = int(input("Enter file iteration: "))
        
    
    #reads in all matrices
    matrix0 = readFile(0)
    matrix1 = readFile(1)
    matrix2 = readFile(2)
    matrix3 = readFile(3)
    matrix4 = readFile(4)
    
    #gets the dimnesions of the matrices
    x0,y0 = getMatrixSize(matrix0)
    x1,y1 = getMatrixSize(matrix1)
    x2,y2 = getMatrixSize(matrix2)
    x3,y3 = getMatrixSize(matrix3)
    x4,y4 = getMatrixSize(matrix4)
    
    #finds the widest and the tallest matrix
    width = max(x0,x1,x2,x3,x4)
    height = max(y0,y1,y2,y3,y4)
    
    #resize all
    if user == 1:
        writeBack((resizeMatrix(matrix0,width,height)))
        writeBack((resizeMatrix(matrix1,width,height)))
        writeBack((resizeMatrix(matrix2,width,height)))
        writeBack((resizeMatrix(matrix3,width,height)))
        writeBack((resizeMatrix(matrix4,width,height)))
    
    #resize one
    elif user == 2:
        
        #resizes only the matrix specified by the user
        if it == 0:
            writeBack((resizeMatrix(matrix0,width,height)))
        elif it == 1:
            writeBack((resizeMatrix(matrix1,width,height)))
        elif it == 2:
            writeBack((resizeMatrix(matrix2,width,height)))
        elif it == 3:
            writeBack((resizeMatrix(matrix3,width,height)))
        elif it == 4:
            writeBack((resizeMatrix(matrix4,width,height)))
            
    user = input("**Hit ENTER to close**")          #keeps the terminal open

#displays the menu
def dispMenu():
    print("----------------------------")
    print("Select on of the following:")
    print("1. Resize all files")
    print("2. Resize one file")
    print("----------------------------")
    return int(input())
    
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

#resizes the matrix based on the new x and y dimensions
def resizeMatrix(matrix,x,y,times = 0):
    oldX, oldY = getMatrixSize(matrix)
    xDif = abs(oldX - x)        #difference between the widths
    yDif = abs(oldY - y)        #difference between the heights
    pbar = ProgressBar((len(matrix) - 1) + (y - int(y/2)) + 1,"Resizing matrix...")
    newMatrix = []
    
    #resizes the width
    if xDif > 0:
        newMatrix = addHorizSpace(matrix,xDif,pbar)
        #for i in range(len(matrix)):
            #for j in range(xDif):       #adds x amount of columns to the right
                #matrix[i].append(0)
        
        #i = len(matrix) - 1        
        #while i >= 0:                                 #adds x amount of columns to the left(shifts the elements to the right)
            #j = len(matrix[i]) - 1
            #while j >= 0:
                #if j != 0:
                    #matrix[i][j] = matrix[i][j - 1]
                    #matrix[i][j - 1] = 0
                    
                #else:
                    #matrix[i][j] = 0
                #j = j - 1
            #i = i - 1    
    
    #resizes the height
    if yDif > 0:
        newMatrix = addVertSpace(newMatrix,yDif,pbar)            #adds x amount of rows to the bottom
        
        #i = len(matrix) - 1
        #while i >= 0:                         #adds x amount of rows to the top
            #j = len(matrix[i]) - 1
            #while j >= 0:
                #if i != 0:
                    #matrix[i][j] = matrix[i - 1][j]
                    #matrix[i - 1][j] = 0
                #else:
                    #matrix[i][j] = 0
                #j = j - 1
            #i = i - 1
    if len(newMatrix) == 0:
        return matrix
    else:
        return newMatrix

#copies the matrix
def addVertSpace(old,y,pbar):
    matrix = []
    
    for row in old:         #copies the old matrix into the new one
        matrix.append(row)
        
        size = int(y/2)
        if size * 2 < y:
            size = size + 1       
        
    for i in range(size): 
        temp = []
        for j in range(len(old[0])):
            temp.append(0)
        matrix.append(row)      #adds the new rows at the bottom                        
        if i + (len(matrix) - 1) < int(y/2) + (len(matrix) -1):
            matrix.insert(0,row)    #adds the new rows at the top of the matrix
        #matrix[i][j] = old[int(i/y)][j]
        pbar.update()
    return matrix

def addHorizSpace(old,x,pbar):
    matrix = []
    
    for row in old:         #copies the old matrix into the new one
        matrix.append(row) 
        
    size = int(x/2)
    if size * 2 < x:
        size = size + 1
        
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):     
            if j < size:
                matrix[i].append(0)     #adds x amount of columns to the right
                if j + (len(matrix) - 1) < int(x/2) + (len(matrix) -1):            
                    matrix[i].insert(0,0)   #adds x amount of columns to the left
            #matrix[i][j] = old[i][int(j/x)]
        pbar.update()
    return matrix

#rescales the old matrix to fit the new dimensions
#def scaleMatrix(matrix,old):
    #y = len(matrix)
    #x = len(matrix[0])
    #oldY = len(old)
    #oldX = (len(old[0]))
    
    #pbar = ProgressBar((y*x) + 1,"Scaling elements...")
    
    #xInc = (x/oldX)
    #yInc = (y/oldY)
    
    #for i in range(y):
        #for j in range(x):
            #matrix[i][j] = old[int(i/yInc)][int(j/xInc)]       
            #pbar.update()
    
    ##y = y - 1
    ##while y > 0 :
        ##x = len(matrix[0]) - 1        
        ##while x > 0:
            ##for k in range(xInc):
                ##if x - k >= 0:
                    ##matrix[y][x - k] = matrix[y][x]
            ##pbar.update()
            ##x = x - 1
        ##y = y - 1
    #return matrix
                
            


#finds the dinesions of the matrix
def getMatrixSize(matrix):
    y = len(matrix)
    x = len (matrix[0])
    return x,y

#writes the matrix to a new file
def writeBack(matrix):
    size = len(matrix) + len(matrix[0]) + int((len(matrix) * len(matrix[0])))
    pbar = ProgressBar(size,"Writing points to file...")    #initializes the progress bar
    line = ""
    i = 0
    
    #gets the appropriate file name
    it = str(getIteration())
    newFile = "./3D Maps(resized)/3D Latitudes(resized)(" + it + ").txt"
    
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
    
    newFile = "./3D Maps(resized)/3D Longitudes(resized)(" + it + ").txt"
    
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
    
    newFile = "./3D Maps(resized)/3D Matrix(resized)(" + it + ").txt"
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
    return    

#gets the iteration of 3D model points generated and updates the iteration count
def getIteration():
    filePath = "./3D Maps(resized)/Iteration.txt"
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