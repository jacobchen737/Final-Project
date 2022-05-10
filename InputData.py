from enum import Enum

# simulation settings
import numpy as np

POP_SIZE = 1000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate


class Treatment(Enum):
    NONE = 0
    HPV_SCREEN = 1
    CRYT_SCREEN = 2
    DUAL_SCREEN = 3

class HealthStates(Enum):
    WELL = 0
    PRE_CANCER = 1
    PRE_CANCER_SCREENING = 2
    PRE_CANCER_TREATMENT = 3
    CANCER = 4
    CANCER_SCREENING = 5
    CANCER_TREATMENT = 6
    CANCER_DEATH = 7
    OTHER_DEATH = 8

#annual cost of each health state
ANNUAL_STATE_COST_SCREENING = [
    0,      #WELL
    0,      #WELL_SCREEENING
    100,    #PRE_CANCER
    0,      #PRE_CANCER_SCREENING (cost of HPV or Cyt)
    0,      #PRE_CANCER_TREATMENT
    56250,   #CANCER


]
# treatment sensitivity
HPV_SCREEN_RR = 0.9260
CRYT_SCREEN_RR = 0.7550
DUAL_SCREEN_RR = 0.9370


ANNUAL_PROB_ALL_CAUSE_MORT = 41.4/1000
ANNUAL_PROB_CERVICALCANCER_MORT = 311000/3904727342
PROB_WELL_PRECANCER = 0.10636
PROB_WELL_CANCER = 0.007
PROB_WELL_WELL = 1 - PROB_WELL_CANCER
PROB_PRECANCER_WELL = 0.6
PROB_PRECANCER_CANCER = 0.4
PROB_CANCER_DEATH = 0.361753675

SCREEN_DURATION = 1/365
PRECANCERTREATMENT_DURATION = 1/4
CANCERTREATMENT_DURATION = 1/2

HPV_SCREEN_FREQUENCY = 1/5
CRYT_SCREEN_FREQUENCY = 1/3
DUAL_SCREEN_FREQUENCY = 1/5

def get trans_rate_matrix(treatment):
 """
 :param with_treatment: to calculate the transition matrix when screening is implemented
 :return: transition rate matrix
 """

# Part 1: find the annual rate of non-cervical-cancer death
annual_prob_non_cervicalcancer_mort = (ANNUAL_PROB_ALL_CAUSE_MORT - ANNUAL_PROB_CERVICALCANCER_MORT)
lambda0 = -np.log(1 - annual_prob_non_cervicalcancer_mort)

# Part 2: lambda 1 + lambda 2 WELL -> PRECANCER
lambda1= -np.log(1 - PROB_WELL_PRECANCER)

# Part 3: WELL -> CANCER
lambda2 = -np.log(1-PROB_WELL_CANCER)

# Part 4: PRECANCERTREATMENT -> WELL
lambda3 = 1/PRECANCERTREATMENT_DURATION

# Part 5: PRECANCER -> CANCER
lambda4 = -np.log(1-PROB_PRECANCER_CANCER)

# Part 6: CANCER -> DEATH
lambda5 = -np.log(1- PROB_CANCER_DEATH)

# Part 7: WELLSCREENING -> PRECANCERTREATMENT
lambda6 = (1/SCREEN_DURATION)*lambda1

# Part 8 WELLSCREENING -> CANCERTREATMENT
lambda7 = (1/SCREEN_DURATION)*lambda2

# Part 9 WELL -> WELL
lambda8 = -np.log(1-PROB_WELL_WELL)

#Part 10 WELLSCREENING -> WELL
lambda9 = (1/SCREEN_DURATION)*lambda8

# Part 11 PRECANCERSCREENING -> CANCERTREATMENT
lambda10 = (1/SCREEN_DURATION)*lambda4

# Part 12 PRECANCERSCREENING -> PRECANCERTREATMENT
lambda11 = (1/SCREEN_DURATION)*lambda3

# Part 13 CANCERTREATMENT -> CANCER
lambda12 = 1/CANCERTREATMENT_DURATION







TRANS_MATRIX_HPV = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_DEATH
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # OTHER_DEATH
    ]

TRANS_MATRIX_CRYT = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_DEATH
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # OTHER_DEATH
    ]


TRANS_MATRIX_DUAL = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # WELL_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # PRE_CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_SCREENING
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # CANCER_DEATH
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # OTHER_DEATH
    ]

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,     # WELL
    0,     # WELL_SCREENING
    0,     # PRE_CANCER
    0,     # PRE_CANCER_SCREENING
    299,   # PRE_CANCER_TREATMENT (cost of colposcopy)
    0,     # CANCER
    0,     # CANCER_SCREENING
    1702,  # CANCER_TREATMENT
    0,     # CANCER_DEATH
    0,     # OTHER_DEATH
    ]

# annual health utility of each health state
# ANNUAL_STATE_UTILITY = [
#     0,  # WELL
#     0,  # HR_HPV
#     0,  # L_DYSPLASIA
#     0,  # H_DYSPLASIA
#     1702,  # CANCER
#     0,  # CANCER_DEATH
#     0,  # OTHER_DEATH
#     ]

# treatment costs
HPV_SCREEN_COST = 117
CRYT_SCREEN_COST = 98
DUAL_SCREEN_COST = 142
#COLPOSCOPY_COST = 299