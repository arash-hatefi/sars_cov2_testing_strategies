from utils import Coordinate, Displacement, get_random_coordinate
from default_parameters import *
from disease_info import DiseaseInfo
from infection_statistics import InfectionStatistics
from individuals import Dead, Infected, Healthy, Susceptible, Exposed, PreSymptomatic, InfectedSymptomatic, InfectedAsymptomatic, Detected, Recovered
from ct import ContantTracing
import numpy as np



class Society:
    

    def __init__(self, 
                 n_individuals=N_INDIVIDUALS_DEFAULT, 
                 lattice_size=LATTICE_SIZE_DEFAULT, 
                 initial_infection_rate=INITIAL_INFECTION_RATE_DEFAULT,
                 moving_rate_range=MOVING_RATE_RANGE_DEFAULT,
                 traced_indididuals_fraction=TRACED_INDIVIDUALS_FRACTION_DEFAULT,
                 n_time_steps_to_trace=N_TIME_STEPS_TO_TRACE_DEFAULT, 
                 initially_tested_population_fraction=INITIALLY_TESTED_POPULATION_FRACTION,
                 disease_info=DiseaseInfo(), 
                 infection_coordinates=[]): 

        assert (type(lattice_size)==int) and (lattice_size>0), "Invalied lattice_size" 
        assert (initial_infection_rate>0) and  (initial_infection_rate<1), "Invalied initial_infection_rate" 
        assert type(disease_info==DiseaseInfo), "Invalied disease_info" 
        assert type(moving_rate_range==list), "Invalied moving_rate_range" 
        assert len(moving_rate_range)==2, "Invalied moving_rate_range" 
        assert max(moving_rate_range)<=1 and min(moving_rate_range)>=0, "Invalied moving_rate_range" 
        
        self.n_individuals = n_individuals
        
        self.initial_infection_rate = initial_infection_rate

        self.disease_info = disease_info
        
        self.lattice_size = lattice_size

        self.n_susceptible = 0
        self.n_exposed = 0
        self.n_presymptomatic = 0
        self.n_asymptomatic = 0
        self.n_symptomatic = 0
        self.n_detected = 0
        self.n_recovered = 0
        self.n_dead = 0
        
        if infection_coordinates==[]:
            for _ in range(int(n_individuals*initial_infection_rate)):
                infection_coordinates.append(get_random_coordinate(self.lattice_size))
        
        self.population = []
        self.infected_spots = set()
        for coordinate in infection_coordinates:
            moving_probability = np.random.uniform(*moving_rate_range)
            self.population.append(PreSymptomatic(coordinate, moving_probability, self.disease_info))
            self.n_presymptomatic += 1
            self.infected_spots.add(coordinate)
        while (len(self.population)!=n_individuals):
            coordinate = get_random_coordinate(self.lattice_size)
            moving_probability = np.random.uniform(*moving_rate_range)
            self.population.append(Susceptible(coordinate, moving_probability, self.disease_info))
            self.n_susceptible += 1

        self.do_contact_tracing = True if (traced_indididuals_fraction>0) else False
        n_ct_ditections = 0
        if self.do_contact_tracing:
            traced_individuals_indices = np.random.permutation(self.n_individuals)[:int(traced_indididuals_fraction*self.n_individuals)]
            self.contact_tracing = ContantTracing(self.population, traced_individuals_indices, n_time_steps_to_trace=n_time_steps_to_trace, lattice_size=self.lattice_size)
            self.contact_tracing.test_random_individuals(int(n_individuals*initially_tested_population_fraction))
            # n_ct_ditections = self.contact_tracing.step_time()
        
        self.log = []
        self.log_info(lockdown_effectiveness=0, n_ct_ditections=0, n_sd_ditections=0)
        
    
    def iterate(self, n_iterations=None, lockdown_iterations=[], lockdown_effectiveness=0, print_results=True, verbose=False):
        
        if (n_iterations==None): n_iterations = np.inf
        if (print_results and verbose): print(f"Iteration {0}:\t\t{self.log[-1]}\t\t\r", end='')
        if (print_results and (not verbose)): print(f"Iteration {0}\t\t\r", end='')
        iteration = 1
        while True:
            lockdown = True if iteration in lockdown_iterations else False
            motion_restriction_coeff = lockdown_effectiveness if lockdown else 0
            self.step_time(motion_restriction_coeff)
            if (print_results and verbose): print(f"Iteration {iteration}:\t\t{self.log[-1]}\t\t\r", end='')
            if (print_results and not verbose): print(f"Iteration {iteration}\t\t\r", end='')
            if ((self.n_exposed+self.n_presymptomatic+self.n_asymptomatic+self.n_symptomatic+self.n_detected)==0 or iteration==n_iterations): 
                break
            iteration += 1
    
    
    def step_time(self, motion_restriction_coeff):
        
        n_ct_ditections = 0
        if (self.do_contact_tracing): 
            n_ct_ditections = self.contact_tracing.step_time()
        
        infected_spots = set()
        susceptible = 0
        exposed = 0
        presymptomatic = 0
        asymptomatic = 0
        symptomatic = 0
        detected = 0
        recovered = 0
        dead = 0
        n_sd_ditections = 0
        
        for idx in range(len(self.population)): 
            exposed_to_infection = True if self.population[idx].coordinate in self.infected_spots else False
            self.population[idx], sd_detected = self.population[idx].step_time(exposed_to_infection, motion_restriction_coeff)
            n_sd_ditections += int(sd_detected)
            individual_type = self.population[idx].type
            if (individual_type==Susceptible):
                susceptible += 1
            elif (individual_type==Exposed):
                exposed += 1
            elif (individual_type==PreSymptomatic):
                presymptomatic += 1
                infected_spots.add(self.population[idx].coordinate)
            elif (individual_type==InfectedAsymptomatic):
                asymptomatic += 1
                infected_spots.add(self.population[idx].coordinate)
            elif (individual_type==InfectedSymptomatic):
                symptomatic += 1
                infected_spots.add(self.population[idx].coordinate)
            elif (individual_type==Detected):
                detected += 1
                infected_spots.add(self.population[idx].coordinate)
            elif (individual_type==Recovered):
                recovered += 1
            elif (individual_type==Dead):
                dead += 1
        
        self.infected_spots = infected_spots
        self.n_susceptible = susceptible
        self.n_exposed = exposed
        self.n_presymptomatic = presymptomatic
        self.n_asymptomatic  = asymptomatic
        self.n_symptomatic = symptomatic
        self.n_detected = detected
        self.n_recovered = recovered
        self.n_dead = dead
        
        self.log_info(motion_restriction_coeff, n_ct_ditections, n_sd_ditections)
        
            
    
    def log_info(self, lockdown_effectiveness, n_ct_ditections, n_sd_ditections):

        self.log.append(InfectionStatistics(self.n_susceptible, 
                                            self.n_exposed,
                                            self.n_presymptomatic, 
                                            self.n_asymptomatic, 
                                            self.n_symptomatic, 
                                            self.n_detected,
                                            self.n_recovered,
                                            self.n_dead,
                                            lockdown_effectiveness, 
                                            n_ct_ditections,
                                            n_sd_ditections))