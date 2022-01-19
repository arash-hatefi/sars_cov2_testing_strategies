import numpy as np



class Coordinate:
    
    MAX_LATTICE_SIZE = 1_000
    PRECISION = 0.0001
    
    def __init__(self, x, y, lattice_size=None):
        
        self.lattice_size = lattice_size
        self.xy = np.array([x, y])
        if (self.lattice_size!=None):
            self.xy = self.xy % self.lattice_size
        

    def __add__(self, other):
          
        xy = None
        if (type(other)==Displacement):
            xy = self.xy + other.xy
        elif (type(other)==int) or (type(other)==float):
            xy = self.xy + other
        else:
            assert (0), f"invalied + operation between {self} and {other}"
        
        if (self.lattice_size!=None):
            xy = xy % self.lattice_size
        return type(self)(*xy, self.lattice_size)
        
    
    def __mul__(self, other):
        
        assert (type(other)==float or type(other)==int), f"invalied * operation between {self} and {other}"
        xy = self.xy * other
        if (self.lattice_size!=None):
            xy = xy % self.lattice_size
        return type(self)(*xy, self.lattice_size)
    
    
    def __rmul__(self, other):
        
        return self.__mul__(other)
    
    
    def __eq__(self, other):
        
        return (self.xy==other.xy).all() and (self.lattice_size==other.lattice_size)
    
    
    def __repr__(self):
        
        return f"Coordinate({self.xy[0]}, {self.xy[1]})"
    
    
    def __str__(self):
        
        return self.__repr__()
    
    
    def __hash__(self):
        
        return int((self.xy[0] * self.MAX_LATTICE_SIZE + self.xy[1])/self.PRECISION)
    
    
    @property
    def tolist(self):

        return self.xy.tolist()



class Displacement(Coordinate):
    

    def __init__(self, x, y, lattice_size=None):

        super().__init__(x, y, lattice_size)

    
    def __repr__(self):
        
        return f"Displacement({self.xy[0]}, {self.xy[1]})"
    
    
    def __str__(self):
        
        return self.__repr__()



def get_random_coordinate(lattice_size):
    
    assert (type(lattice_size)==int)
    
    xy = np.random.randint(lattice_size, size=(2,))
    
    return Coordinate(*xy, lattice_size)