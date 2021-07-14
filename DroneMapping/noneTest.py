from progressBar import ProgressBar
def test():
    p = int(input("Enter file iteration: "))
    fileName="3D Maps/3D Matrix("+str(p)+").txt"
    x=0
    count = 0
    no = 0
    temp = []
    pbar = ProgressBar(getFileSize(fileName),"Reading in...")
    file = open(fileName)
    for line in file:
        x+=1
        if x > 2:
            vals = line.rstrip().split(",")
            for element in vals:
                if element == "None" or element == None:
                    no+=1
            pbar.update()
            count+= len(vals)
        else:
            pbar.update()
    file.close()
    print()
    print("Lines in file............= ",x)
    print("Elements in file.........= ",count)
    print("Number of None types.....= ",no)
    print("Number of not None types.= ",count-no)
    
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

test()