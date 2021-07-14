from progressBar import ProgressBar
def test():
    temp1 = [None,3,5,None,4,3,None]
    temp2 = [2,4,None,None,None,4,6]
    temp3 = [4,None,5,None,6,None,9]
    
    tempN = [None,None,None,None,None,None,None]
    tempN2 = [None,None,None,None,None,None,None]
    tempE = [None,None,4,None,None,None,None]
    
    tT1 = [5,8,4,4,7]
    tT2 = [None,None,None,None,None]
    tT3 = [5,4,2,0,1]
    tT4 = [None,4,2,None,None]
    table = [tT1,tT2,tT4]
    #table = [temp1,temp2,temp3]
    #loc = findMissingLocation(temp1)
    #print(findNearest(temp1,6,True,False))
    #temp1 = solveMissing(loc,temp1,1)  
    #for element in temp1:
        #print(element,",",end="")
    
    for row in table:
        for element in row:
            print(element,",",end="")
        print()    
        
    table = findAllMissing(table)
    for row in table:
        for element in row:
            print(element,",",end="")
        print()
    
#finds all missing data and solves for it in a 2D array
def findAllMissing(table,acc = 0):      #acc = 0 is normal accuracy         acc = 1 is high accuracy
    pos = 0
    size = len(table)
    if acc == 1:
        size = size * 2
    pbar = ProgressBar(size,"Packing Matrix...")
    
    while pos < len(table):
        table[pos] = solveMissing(table,pos)
        pos = pos + 1
        pbar.update()
    
    #high accuracy
    if acc == 1:
        pos = 0
        while pos < len(table):
            table[pos] = solveMissing(table,pos)
            pos = pos + 1
            pbar.update()        
    return table  
    
#solves for all missing data in an array using the surrounding elements
def solveMissing(matrix,rowPos):
    total = 0
    count = 0
    for i in range(len(matrix[0])):
        count = 0
        total = 0
        #if matrix[rowPos][i] == None or matrix[rowPos][i] >= 0:
        if rowPos > 0 and matrix[rowPos - 1][i] != None:
            total = total + matrix[rowPos - 1][i]
            count = count + 1
            if i > 0 and matrix[rowPos - 1][i - 1] != None:
                total = total + matrix[rowPos - 1][i - 1]
                count = count + 1                
            if i < len(matrix[0])-1 and matrix[rowPos - 1][i + 1]:
                total = total + matrix[rowPos - 1][i + 1]
                count = count + 1                
        if rowPos < len(matrix)-1 and matrix[rowPos + 1][i] != None:
            total = total + matrix[rowPos + 1][i]
            count = count + 1            
            if i > 0 and matrix[rowPos + 1][i - 1] != None:
                total = total + matrix[rowPos + 1][i - 1] 
                count = count + 1                
            if i < len(matrix[0])-1 and matrix[rowPos + 1][i + 1]:
                total = total + matrix[rowPos + 1][i + 1]
                count = count + 1                
        if i > 0 and matrix[rowPos][i - 1] != None:
            total = total + matrix[rowPos][i - 1]
            count = count + 1            
        if i < len(matrix[0])-1 and matrix[rowPos][i + 1] != None:
            total = total + matrix[rowPos][i + 1] 
            count = count + 1
            
        if count > 0:
            matrix[rowPos][i] =  round(total/count,3)
        else:
            matrix[rowPos][i] = 0
    return matrix[rowPos]
#test()