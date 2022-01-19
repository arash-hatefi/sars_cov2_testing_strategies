from default_parameters import *


class DiseaseInfo:
    
    
    def __init__(self,
                 infection_probability=INFECTION_PROBABILITY_DEFAULT,
                 becoming_presymptomatic_probability=BECOMING_PRESYMPATIC_ROBABILITY_DEFAULT,
                 becoming_contagious_probability=BECOMING_CONTAGIOUS_PROBABILITY_DEFAULT,
                 symptomatic_infection_probability=SYMPTOMATIC_INFECTION_PROBABILITY_DEFAULT,
                 symptomatic_detection_probability=SYMPTOMATIC_DETECTION_PROBABILITY_DEFAULT,
                 recovery_after_detection_probability=RECOVERY_AFTER_DETECTION_PROBABILITY_DEFAULT,
                 recovery_without_detection_probability=RECOVERY_WITHOUT_DETECTION_PROBABILITY_DEFAULT,
                 fatality_after_detection_probability=FATALITY_AFTER_DETECTION_PROBABILITY_DEFAULT,
                 fatality_before_detection_probability=FATALITY_BEFORE_DETECTION_PROBABILITY_DEFAULT,
                 immunity_probability=IMMUNITY_PROBABILITY):
        
        self.infection_probability = infection_probability
        self.becoming_presymptomatic_probability = becoming_presymptomatic_probability
        self.becoming_contagious_probability = becoming_contagious_probability
        self.symptomatic_infection_probability = symptomatic_infection_probability
        self.symptomatic_detection_probability = symptomatic_detection_probability
        self.recovery_after_detection_probability = recovery_after_detection_probability
        self.recovery_without_detection_probability = recovery_without_detection_probability
        self.fatality_after_detection_probability = fatality_after_detection_probability
        self.fatality_before_detection_probability = fatality_before_detection_probability
        self.immunity_probability = immunity_probability
        

    def __repr__(self):

        return f"Infection Probability: {self.infection_probability}\n"\
               f"Becoming Presymptomatic Probability: {self.becoming_presymptomatic_probability}\n"\
               f"Becoming Contagious Probability: {self.becoming_contagious_probability}\n"\
               f"Symptomatic Infection Probability: {self.symptomatic_infection_probability}\n"\
               f"Symptomatic Detection Probability: {self.symptomatic_detection_probability}\n"\
               f"Recovery After Detection Probability: {self.recovery_after_detection_probability}\n"\
               f"Recovery Without Detection Probability: {self.recovery_without_detection_probability}\n"\
               f"Fatality After Detection Probability: {self.fatality_after_detection_probability}\n"\
               f"Fatality Before Detection Probability: {self.fatality_before_detection_probability}\n"\
               f"Immunity Probability: {self.immunity_probability}"
        
    
    def __str__(self):
        
        return self.__repr__()