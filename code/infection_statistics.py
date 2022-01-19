class InfectionStatistics:
    
    
    def __init__(self, 
                 n_susceptible, 
                 n_exposed,
                 n_presymptomatic, 
                 n_asymptomatic, 
                 n_symptomatic, 
                 n_detected,
                 n_recovered,
                 n_dead,
                 lockdown_effectiveness,
                 n_ct_detections,
                 n_sd_detections):
        
        self.n_susceptible = n_susceptible
        self.n_exposed = n_exposed
        self.n_presymptomatic = n_presymptomatic
        self.n_asymptomatic  = n_asymptomatic
        self.n_symptomatic = n_symptomatic
        self.n_detected = n_detected
        self.n_recovered = n_recovered
        self.n_dead = n_dead
        self.lockdown_effectiveness = lockdown_effectiveness
        self.n_ct_detections = n_ct_detections
        self.n_sd_detections = n_sd_detections
        
        
    def __repr__(self):

        return f'Number of Susceptible: {self.n_susceptible}\n'\
               f'Number of Exposed: {self.n_exposed}\n'\
               f'Number of Presymptomatic: {self.n_presymptomatic}\n'\
               f'Number of Asymptomatic: {self.n_asymptomatic}\n'\
               f'Number of Symptomatic: {self.n_symptomatic}\n'\
               f'Number of Detected: {self.n_detected}\n'\
               f'Number of Recovered: {self.n_recovered}\n'\
               f'Number of Dead: {self.n_dead}\n'\
               f'Lockdown Effectiveness: {self.lockdown_effectiveness}'
        
    
    def __str__(self):
        
        return self.__repr__()