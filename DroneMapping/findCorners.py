

def test():
    t1 = [0,0,0,0,0,0,0,0,0]
    t2 = [0,0,5,4,0,0,0,0,0]
    t3 = [0,0,4,5,4,4,0,0,0]
    t4 = [0,0,4,4,5,5,4,0,0]
    t5 = [0,0,4,5,4,4,4,0,0]
    t6 = [0,0,0,0,5,4,4,5,0]
    t7 = [0,0,0,0,0,0,0,0,0]
    temp = []
    
    temp.append(t1)
    temp.append(t2)
    temp.append(t3)
    temp.append(t4)
    temp.append(t5)
    temp.append(t6)
    temp.append(t7)
    
    c = findAllCorners(temp)
    
    for element in c:
        print(element)



#finds all corners of the building
def findAllCorners(matrix):
    i = -1
    j = -1
    corners = []    
    
    while i <= 2:
        j = -1
        while j < 2:
            corners.append(findCorner(matrix,i,j))
            j = j + 2
        i = i + 2
    return validate(matrix,corners)

#finds a corner of the building
'''      c1                c3
         -------------------
         |                 |
         |                 |
         -------------------
         c2                c4
'''
def findCorner(matrix,vert,horiz):
    #finds the middle of the matrix
    predX = None
    predY = None
    startX = int(len(matrix)/2)
    startY = int(len(matrix[0])/2)
    
    while startX > 0 and startX < len(matrix):
        if matrix[startX+horiz][startY+vert] < 2.7 and matrix[startX-horiz][startY] < 2.7 and matrix[startX][startY+vert] < 2.7:     #if its at a corner
            break
        elif predX == startX and predY == startY:
            break
        
        #updates the previous x and y
        predX = startX
        predY = startY        
        
        #changes the y value if necessary
        while startY > 0 and startY < len(matrix[0]):
            if matrix[startX][startY + vert] <= 2.7:
                break
            elif matrix[startX][startY + vert] >= 2.7:      #increments y if necessary
                startY = startY + vert
            if matrix[startX + horiz][startY] >= 2.7:      #increments x if necessary
                startX = startX + horiz            
        if matrix[startX + horiz][startY] >= 2.7:      #increments x if necessary
            startX = startX + horiz
        
        #if the last item is diagnol
        if matrix[startX + horiz][startY + vert] >= 2.7:
            startX = startX + horiz
            startY = startY + vert
    
    return startX, startY

#validates the corners and updates them if necessary
def validate(matrix, corners):
    vals = [None,None,None,None]
    k = -2
    j = 0
    l = -4
    for element in corners:
        #print(element)
        vals[j] = matrix[element[0]][element[1]]
        if k < 0:
            i = 0
        else:
            i = len(matrix[0]) - 1
        if l < 0:
            m = 0
        else:
            m = len(matrix) - 1
        for e in matrix[element[0]]:
            if matrix[element[0]][i] == matrix[element[0]][element[1]]:
                break
            elif matrix[element[0]][i] >= 2.8 and i < element[1] + 10 and i > element[1]:
                #print(matrix[element[0]][i],i)
                vals[j] = matrix[element[0]][i]
            if k < 0:
                i += 1
            else:
                i -= 1   
            for el in matrix:
                if matrix[m][element[1]] == matrix[element[0]][element[1]]:
                    break
                elif matrix[m][element[1]] >= 2.8 and matrix[m][element[1]] <= 3 and m < element[1] + 10 and m > element[1]:
                    #print(matrix[element[0]][i],i)
                    vals[j] = matrix[m][element[1]]
                if l < 0:
                    m += 1
                else:
                    m -= 1                   
        k += 1
        j += 1
        l = (l + 1) * -1 
    return vals

#test()
            