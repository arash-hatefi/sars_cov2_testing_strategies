import numpy as np
from collections import deque
from individuals import Dead, Infected, Healthy, Susceptible, Exposed, PreSymptomatic, InfectedSymptomatic, InfectedAsymptomatic, Detected, Recovered



class ContantTracing:


    def __init__(self, population, traced_individuals_indices, n_time_steps_to_trace, lattice_size):

        assert(np.min(traced_individuals_indices)>=0 and np.max(traced_individuals_indices)<len(population) and traced_individuals_indices.dtype==int), "Invalied traced_individuals_indices"
        self.population = population
        self.n_population = len(population)
        self.traced_individuals_indices = traced_individuals_indices
        self.lattice_size = lattice_size
        self.contacts = [deque(maxlen=n_time_steps_to_trace) if i in self.traced_individuals_indices else None for i in range(self.n_population)]


    def get_lattice(self):   
        
        lattice = [[[] for _ in range(self.lattice_size)] for _ in range(self.lattice_size)]
        for individual_idx in self.traced_individuals_indices:
            coordinate = self.population[individual_idx].coordinate
            lattice[coordinate.xy[0]][coordinate.xy[1]].append(individual_idx)
        return lattice


    def get_positive_detected_individuals(self):

        positive_detected_individuals = set()
        for individual_idx in self.traced_individuals_indices:
            individual_type = self.population[individual_idx].type
            if (individual_type==Detected):
                positive_detected_individuals.add(individual_idx)
        return positive_detected_individuals


    def update_contacts(self):

        lattice = self.get_lattice()
        for individual_idx in self.traced_individuals_indices:
            coordinate = self.population[individual_idx].coordinate
            self.contacts[individual_idx].append(lattice[coordinate.xy[0]][coordinate.xy[1]])
    
    
    def step_time(self):

        self.update_contacts()
        probably_infected_individuals_indices = []
        for individual_idx in self.get_positive_detected_individuals():
            for contacts_in_each_time_step in self.contacts[individual_idx]:
                probably_infected_individuals_indices.extend(contacts_in_each_time_step)
            self.contacts[individual_idx].clear()
        n_detections = self.test_individuals(set(probably_infected_individuals_indices))
        return n_detections

    
    def test_individuals(self, individuals_indices):

        n_detections = 0
        for individual_idx in individuals_indices:
            if (self.population[individual_idx].type!=Detected):
                self.population[individual_idx] = self.population[individual_idx].test_for_disease()
                if (self.population[individual_idx].type==Detected):
                    n_detections += 1
        return n_detections


    def test_random_individuals(self, n_tests):

        sellected_indices = np.random.permutation(self.traced_individuals_indices)[:n_tests]
        _ = self.test_individuals(sellected_indices)