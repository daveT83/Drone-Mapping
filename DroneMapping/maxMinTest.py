from progressBar import ProgressBar

def main():
    altMax = None
    altMin = None
    fileName = input("Enter file name: ")
    fileName = "./Drone Data/" + fileName
    it = (input("Enter iteration: "))    
    it = "./3D Maps/3D Matrix("+it+").txt"
    
    size = getFileSize(fileName)
    
    pbar = ProgressBar(size,"Reading in data...")  
    
    #reads in the data from the file
    file = open(fileName)
    for line in file:   
        points = []
        vals = line.rstrip().split(',')
        for element in vals:
            temp = element.split(' ')
            points.append(temp[len(temp)-1])
        vals = points        
        
        #determine the max altitude
        if altMax == None:
            altMax = abs(float(vals[2]))
            altMin = abs(float(vals[2]))
        elif abs(float(vals[2])) > altMax:
            altMax = abs(float(vals[2]))
        elif abs(float(vals[2])) < altMin:
            altMin = abs(float(vals[2]))
            
        pbar.update()       #updates the prgress bar
    file.close()            #closes the file
    
    maxM,minM = maxMatrix(it)
    
    print("Max altitude in matrix.= ",maxM)
    print("Min altitude in matrix.= ",minM)
    print("Max altitude...........= ",altMax)
    print("Min altitude...........= ",altMin)
    
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

def maxMatrix(it):
    i = 0
    lineNum = 0
    altMax = None
    altMin = None
    
    size = getFileSize(it)
    
    pbar = ProgressBar(size,"Reading in data...")  
    
    #reads in the data from the file
    file = open(it)
    for line in file:   
        points = []
        vals = line.rstrip().split(',')        
        
        #determine the max altitude
        for element in vals:
            if altMin == None and float(element) > 2.4384:
                altMin = float(element)
            elif altMin != None and float(element) < altMin and float(element) >= 2.4384:
                altMin = float(element)            
            if altMax == None:
                altMax = float(element)
            elif float(element) > altMax:
                altMax = float(element) 
                lineNum = i
        i += 1
        pbar.update()
    file.close()
    return altMax,altMin


main()