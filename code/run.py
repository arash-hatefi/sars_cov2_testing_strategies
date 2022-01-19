from default_parameters import *
from disease_info import DiseaseInfo
from society import Society
import numpy as np


n_iterations = 1000

disease_info = DiseaseInfo(infection_probability=INFECTION_PROBABILITY_DEFAULT,
                           becoming_presymptomatic_probability=BECOMING_PRESYMPATIC_ROBABILITY_DEFAULT,
                           becoming_contagious_probability=BECOMING_CONTAGIOUS_PROBABILITY_DEFAULT,
                           symptomatic_infection_probability=SYMPTOMATIC_INFECTION_PROBABILITY_DEFAULT,
                           symptomatic_detection_probability=SYMPTOMATIC_DETECTION_PROBABILITY_DEFAULT,
                           recovery_after_detection_probability=RECOVERY_AFTER_DETECTION_PROBABILITY_DEFAULT,
                           recovery_without_detection_probability=RECOVERY_WITHOUT_DETECTION_PROBABILITY_DEFAULT,
                           fatality_after_detection_probability=FATALITY_AFTER_DETECTION_PROBABILITY_DEFAULT,
                           fatality_before_detection_probability=FATALITY_BEFORE_DETECTION_PROBABILITY_DEFAULT,
                           immunity_probability=IMMUNITY_PROBABILITY)

society = Society(n_individuals=N_INDIVIDUALS_DEFAULT, 
                  lattice_size=LATTICE_SIZE_DEFAULT, 
                  initial_infection_rate=INITIAL_INFECTION_RATE_DEFAULT,
                  moving_rate_range=MOVING_RATE_RANGE_DEFAULT,
                  traced_indididuals_fraction=TRACED_INDIVIDUALS_FRACTION_DEFAULT,
                  n_time_steps_to_trace=N_TIME_STEPS_TO_TRACE_DEFAULT, 
                  initially_tested_population_fraction=INITIALLY_TESTED_POPULATION_FRACTION,
                  disease_info=disease_info)

society.iterate(n_iterations=n_iterations, print_results=True, verbose=True)