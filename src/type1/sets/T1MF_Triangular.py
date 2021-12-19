"""
T1MF_Triangular.py
Created 17/12/2021
"""

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from type1.sets.T1MF_Singleton import T1MF_Singleton

class T1MF_Triangular(T1MF_Prototype):
    """
    Class T1MF_Triangular
    The triangular membership function for type 1 fuzzy sets

    Parameters: 
        name: The name of the membership function
        peak: the current peak
        start: Start of triangle
        end: End of the triangle

    Functions:
        getFS
        getStart
        getPeak
        getEnd
        toString
        compareTo
        getAlphaCut
        findLinearEquationParameters
        
    """

    def __init__(self, name,start,peak,end) -> None:
        super().__init__(name)
        #left and right "leg" slope
        self.lS = None
        self.rS = None
        #left and right "leg" intercept   
        self.lI = None
        self.rI = None
        self.start = start
        self.peak = peak
        self.end = end
        self.support = Tuple(start,end)

    def getFS(self, x) -> float:
        """Return the maximum FS between two sets"""
        if (self.isLeftShoulder and x <= self.peak) or (self.isRightShoulder and x >= self.peak):
            return 1.0
        
        if x<self.peak and x>self.start:
            out = (x-self.start)/(self.peak-self.start)
        elif x == self.peak:
            out = 1.0
        elif x>self.peak and x<self.end:
            out = (self.end-x)/(self.end-self.peak)
        else:
            out = 0.0
        
        return out
    
    def getStart(self) -> float:
        """Get the start value of the function"""
        return self.start
    
    def getPeak(self) -> float:
        """Get the peak value of the function"""
        return self.peak
    
    def getEnd(self) -> float:
        """Get the end value of the function"""
        return self.end

    def toString(self) -> str:
        """Convert membership function to string"""
        s = self.name+"  -  "+str(self.start)+"  "+str(self.peak)+"  "+str(self.end)
        if self.isLeftShoulder():
            s += " (LeftShoulder)"
        if self.isRightShoulder():
            s += " (RightShoulder)"
        return s

    def compareTo(self, o) -> int:
        """Compare the function against triangular or singleton functions"""
        if type(o) is T1MF_Triangular:
            if self.getEnd() == o.getEnd() and self.getStart() == o.getStart() and self.getPeak() == o.getPeak():
                return 0
            if self.getEnd() <= o.getEnd() and self.getStart() <= o.getStart() and self.getPeak() <= o.getPeak():
                return -1
            return 1
        elif type(o) is T1MF_Singleton:
            if self.getPeak() < o.getValue():
                return -1
            return 1
        else:
            raise Exception("A T1MF_Triangular object or T1MF_Singleton is expected for comparison with another T1MF_Triangular object.")
        
    def getAlphaCut(self, alpha) -> Tuple:
        """Get the alpha cut as a tuple"""
        self.findLinearEquationParameters()
        return Tuple((alpha-self.lI)/self.lS,(alpha-self.rI)/self.rS)
    
    def findLinearEquationParameters(self) -> None:
        """Finds the slopes and intercepts for the left and right "leg" of the membership function.
        If the parameters for the given set have previously been computed, the method returns directly."""
        if not self.lS == None:
            return
  
        self.lS = 1.0 / (self.peak-self.start);
        self.lI = 0 - self.lS * self.start;
        

        self.rS = -1.0 / (self.end-self.peak);
        self.rI = 0 - self.rS * self.end;  
    