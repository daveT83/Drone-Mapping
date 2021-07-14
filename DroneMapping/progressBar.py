from math import floor
from time import clock

def test():
    pbar = ProgressBar(10,"Testing")
    x = 0
    while x < 10:
        pbar.update()
        x+=1

class ProgressBar():
    total = 0
    done = 0
    title = ""
    loadingChar = '#'
    blankChar = '-'
    lastUp = 0
    
    
    def __init__(self,numElements,name = ""):
        self.total = numElements
        self.title = name
        clock()
        return

    #updates the progress bar
    def update(self,increment = 1):
        self.done = increment + self.done
        if clock() - (self.lastUp) >= .1:
            self.lastUp = clock()
            percentage = 100*(self.done/self.total)
            temp = floor(50*(self.done/self.total))
            print(self.title,"[",self.loadingChar*temp,self.blankChar*(50-temp),"]",self.done,"/",self.total," %3.2f"%percentage,"%", end='\r') 
        if self.done >= self.total:
            temp = floor(50*(self.done/self.total))
            print(self.title,"[",self.loadingChar*temp,self.blankChar*(50-temp),"]",self.done,"/",self.total," 100.00%")
            print()
        return
    
    #sets all class variables to None to save memory
    def close(self):
        self.total = None
        self.done = None
        self.lastUp = None
        self.title= None
        self.loadingChar = None
        self.blankChar = None
        
    #returns the number of actions done
    def getDone(self):
        return self.done
    
    #returns teh number of expected actions
    def getTotal(self):
        return self.total
        
        

#test()
    
        
