import numpy as np
from abc import ABC, abstractmethod
from disease_info import DiseaseInfo
from default_parameters import *
from utils import Coordinate, Displacement, get_random_coordinate



class Individual(ABC):
    

    VALIED_MOVING_DIRECTIONS = [Displacement(1,0), 
                                Displacement(0,1), 
                                Displacement(-1,0), 
                                Displacement(0,-1)]
    
    
    def __init__(self, coordinate, moving_probability, disease_info):
        
        assert (type(coordinate)==Coordinate), "Invalied coordinate"
        assert (type(disease_info)==DiseaseInfo), "Invalied disease info"
        assert (moving_probability<=1 and moving_probability>=0), "Invalied moving probability"
        self.coordinate = coordinate
        self.disease_info = disease_info
        self.moving_probability = moving_probability
    
    
    @abstractmethod
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        pass
    
    
    def update_position(self, motion_restriction_coeff=0):

        if (np.random.uniform()<((1-motion_restriction_coeff)*self.stage_movemet_freedom*self.moving_probability)):
            self.move()
            
    
    def move(self):
        
        direction = self.select_random_direction()
        self.coordinate += direction
            
    
    def select_random_direction(self):
        
        movement_idx = np.random.randint(len(self.VALIED_MOVING_DIRECTIONS))
        return self.VALIED_MOVING_DIRECTIONS[movement_idx]
           
        
    @property
    def type(self):

        return type(self)


    @property
    def stage_movemet_freedom(self):

        return 1.


    @abstractmethod
    def test_for_disease(self):

        pass



class Dead(Individual):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        return self, False

    @property
    def stage_movemet_freedom(self):

        return 0
        

    def test_for_disease(self):

        return self



class Infected(Individual):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    @abstractmethod
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        pass


    def test_for_disease(self):
        
        if (np.random.uniform()<TEST_ACCURACY):
            return Detected(self.coordinate, self.moving_probability, self.disease_info)
        return self



class Healthy(Individual):
    

    def __init__(self, coordinate, moving_probability, disease_info, infected_before):
        
        super().__init__(coordinate, moving_probability, disease_info)
        self.infected_before = infected_before


    @property
    @abstractmethod
    def immunity_probability(self):
        pass


    def test_for_disease(self):
        
        if (np.random.uniform()<TEST_ACCURACY):
            return self
        return Detected(self.coordinate, self.moving_probability, self.disease_info)



class Susceptible(Healthy):
    

    def __init__(self, coordinate, moving_probability, disease_info, infected_before=False):
        
        super().__init__(coordinate, moving_probability, disease_info, infected_before)


    @property
    def immunity_probability(self):
        
        return 0

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        if (exposed_to_infection and (np.random.uniform()<self.disease_info.infection_probability) and (np.random.uniform()<1-self.immunity_probability)):
            individual = Exposed(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, False



class Exposed(Infected):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        if (np.random.uniform()<self.disease_info.becoming_presymptomatic_probability):
            individual = PreSymptomatic(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, False



class PreSymptomatic(Infected):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        if (np.random.uniform()<self.disease_info.becoming_contagious_probability):
            if (np.random.uniform()<self.disease_info.symptomatic_infection_probability):
                individual = InfectedSymptomatic(self.coordinate, self.moving_probability, self.disease_info)
            else:
                individual = InfectedAsymptomatic(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, False



class InfectedSymptomatic(Infected):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        r = np.random.uniform()
        sd = False
        if (r<self.disease_info.symptomatic_detection_probability):
            individual = Detected(self.coordinate, self.moving_probability, self.disease_info)
            sd = True
        elif (r<self.disease_info.symptomatic_detection_probability+
                self.disease_info.recovery_without_detection_probability):
            individual = Recovered(self.coordinate, self.moving_probability, self.disease_info)
        elif (r<self.disease_info.symptomatic_detection_probability+
                self.disease_info.recovery_without_detection_probability+
                self.disease_info.fatality_before_detection_probability):
            individual = Dead(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, sd 

    
    @property
    def stage_movemet_freedom(self):

        return PRESYMPTOMATIC_STAGE_MOVEMENT_FREEDOM



class InfectedAsymptomatic(Infected):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        r = np.random.uniform()
        if (r<self.disease_info.recovery_without_detection_probability):
            individual = Recovered(self.coordinate, self.moving_probability, self.disease_info)
        elif (r<self.disease_info.recovery_without_detection_probability+
                self.disease_info.fatality_before_detection_probability):
            individual = Dead(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, False



class Detected(Infected):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info)

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        r = np.random.uniform()
        if (r<self.disease_info.recovery_after_detection_probability):
            individual = Recovered(self.coordinate, self.moving_probability, self.disease_info)
        elif (r<self.disease_info.recovery_after_detection_probability+
                self.disease_info.fatality_after_detection_probability):
            individual = Dead(self.coordinate, self.moving_probability, self.disease_info)
        individual.update_position(motion_restriction_coeff)
        return individual, False 


    @property
    def stage_movemet_freedom(self):

        return DETECTED_STAGE_MOVEMENT_FREEDOM



class Recovered(Healthy):
    

    def __init__(self, coordinate, moving_probability, disease_info):
        
        super().__init__(coordinate, moving_probability, disease_info, infected_before=True)


    @property
    def immunity_probability(self):
        
        return self.disease_info.immunity_probability

    
    def step_time(self, exposed_to_infection, motion_restriction_coeff=0):

        individual = self
        if (np.random.uniform()<1-self.immunity_probability):
            individual = Susceptible(self.coordinate, self.moving_probability, self.disease_info, infected_before=True)
        individual.update_position(motion_restriction_coeff)
        return individual, False