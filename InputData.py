from enum import Enum
import numpy as np

# simulation settings
POP_SIZE = 1000         # cohort population size
SIMULATION_LENGTH = 50    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
class Treatment(Enum):
    NONE = 0
    HPV_SCREEN = 1
    CRYT_SCREEN = 2
    DUAL_SCREEN = 3

class HealthStates(Enum):
    WELL = 0
    WELL_SCREENING = 1
    PRE_CANCER = 2
    PRE_CANCER_SCREENING = 3
    PRE_CANCER_TREATMENT = 4
    CANCER = 5
    CANCER_SCREENING = 6
    CANCER_TREATMENT = 7
    CANCER_DEATH = 8
    OTHER_DEATH = 9

# treatment sensitivity
HPV_SCREEN_SENS = 0.9260
CRYT_SCREEN_SENS = 0.755
DUAL_SCREEN_SENS = 0.9370

# treatment specificity
HPV_SCREEN_SPEC = 0.893
CRYT_SCREEN_SPEC = 0.919
DUAL_SCREEN_SPEC = 0.858

SCREEN_RR = 0

# annual cost of each health state
ANNUAL_STATE_COST_SCREENING = [
    0,     # WELL
    0,     # WELL_SCREENING
    100,   # PRE_CANCER
    0,     # PRE_CANCER_SCREENING
    0,     # PRE_CANCER_TREATMENT (cost of colposcopy)
    1000,  # CANCER
    0,     # CANCER_SCREENING
    0,     # CANCER_TREATMENT
    0,     # CANCER_DEATH
    0,     # OTHER_DEATH
    ]

ANNUAL_STATE_COST_NOSCREENING = [
    0,     # WELL
    1000,     # CANCER
    0,   # CANCER_TREATMENT
    0,     # CANCER_DEATH
    0,     # OTHER_DEATH
    ]


ANNUAL_PROB_ALL_CAUSE_MORT = 8.5 / 1000
ANNUAL_PROB_CERVICALCANCER_MORT = 311000 / 3904727342
PROB_WELL_PRECANCER = 0.10636
PROB_WELL_CANCER = 0.007
PROB_WELL_WELL = 1-PROB_WELL_CANCER-PROB_WELL_PRECANCER
PROB_PRECANCER_WELL = 0.6
PROB_PRECANCER_CANCER = 0.4
PROB_PRECANCER_PRECANCER = 0.5
PROB_CANCEL_DEATH = 0.361753675
PROB_CANCER_CANCER = 0.92

SCREEN_DURATION = 1/365  # 1 day
PRECANCERTREATMENT_DURATION = 1/365 # 1 day for colposcopy
CANCERTREATMENT_DURATION = 2  # 2 years

HPV_SCREEN_FREQUENCY = 5
CRYT_SCREEN_FREQUENCY = 3
DUAL_SCRREN_FREQUENCE = 5

def get_trans_rate_matrix(with_treatment):
    """
    :param with_treatment:  to calculate the transition rate matrix when the anticoagulation is used

    :return: transition rate matrix
    """
    #  WELL->WELLSCREENING  PRECANCER->PRECANCERSCREEN
    if with_treatment == Treatment.HPV_SCREEN:
        lambda13 = 1 / HPV_SCREEN_FREQUENCY
        sens = HPV_SCREEN_SENS
        spec = HPV_SCREEN_SPEC

    if with_treatment == Treatment.CRYT_SCREEN:
        lambda13 = 1 / CRYT_SCREEN_FREQUENCY
        sens = CRYT_SCREEN_SENS
        spec = CRYT_SCREEN_SPEC

    if with_treatment == Treatment.DUAL_SCREEN:
        lambda13 = 1 / DUAL_SCRREN_FREQUENCE
        sens = DUAL_SCREEN_SENS
        spec = DUAL_SCREEN_SPEC


    # Part 1: find the annual probability of non-cervical-cancer death
    annual_prob_non_cervicalcancer_mort = (ANNUAL_PROB_ALL_CAUSE_MORT - ANNUAL_PROB_CERVICALCANCER_MORT)
    lambda0 = -np.log(1 - annual_prob_non_cervicalcancer_mort)

    # Part 2: lambda 1  WELL->PRECANCER
    lambda1 = -np.log(1 - PROB_WELL_PRECANCER)

    # Part 3 WELL->CANCER
    lambda2 = -np.log(1 - PROB_WELL_CANCER)

    # Part 4 PRECANCERTREATMENT->WELL
    lambda3 = 1 / PRECANCERTREATMENT_DURATION

    # Part 5 PRECANCER->CANCER
    lambda4 = -np.log(1 - PROB_PRECANCER_CANCER)

    # part 6 CANCER->DEATH
    lambda5 = -np.log(1 - PROB_CANCEL_DEATH)

    # Part 7 WELLSCREENING->PRECANCERTREATMENT
    lambda6 = (1 / SCREEN_DURATION)*PROB_WELL_PRECANCER

    # part 8 WELLSCREENING->CANCERTREATMENT
    lambda7 = (1 / SCREEN_DURATION)*PROB_WELL_CANCER

    # WELL->WELL
    lambda8 = -np.log(1 - PROB_WELL_WELL)

    # WELLSCREENING->WElL
    lambda9 = (1/SCREEN_DURATION)*PROB_WELL_WELL

    # PRECANCERSCREENING->CANCERTREATMENT
    lambda10 = (1/SCREEN_DURATION)*PROB_PRECANCER_CANCER

    #  PRECANCERSCREENING->PRECANTREATMENT
    lambda11 = (1/SCREEN_DURATION)*(1-PROB_PRECANCER_CANCER)

    #  CANCERTREATMENT->CANCER
    lambda12 = 1/CANCERTREATMENT_DURATION

    # PRECANCER -> PRECANCER
    lambda14 = -np.log(1-PROB_PRECANCER_PRECANCER)

    # CANCER -> CANCER
    lambda15 = -np.log(1-PROB_CANCER_CANCER)


    rate_matrix = [
        [lambda8, lambda2, 0, 0, lambda0],   # WELL
        [0, 0, lambda12, 0, 0],   # CANCER TREATMENT
        [0, 0, 0, lambda5, 0],   # CANCER
        [0, 0, 0, 0, 0],   # CANCER_DEATH
        [0, 0, 0, 0, 0]    # OTHER_DEATH
    ]
    if with_treatment == Treatment.NONE:
        pass
    else:
        rate_matrix = [
            [lambda8, lambda13, lambda1, 0, 0, lambda2, 0, 0, 0, lambda0],  # WELL
            [(1/SCREEN_DURATION)*spec, 0, 0, 0, (1/SCREEN_DURATION)*(1-spec), 0, 0, 0, 0, 0],  # WELL_SCREENING
            [0, 0, lambda14, lambda13, 0, lambda4, 0, 0, 0, lambda0],  # PRE_CANCER
            [0, 0, (1/SCREEN_DURATION)*(1-sens), 0, (1/SCREEN_DURATION)*sens, 0, 0, 0, 0, 0],  # PRE_CANCER_SCREENING
            [lambda3, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # PRE_CANCER_TREATMENT
            [0, 0, 0, 0, 0, lambda15, lambda13, 0, lambda5, lambda0],  # CANCER
            [0, 0, 0, 0, 0, (1/SCREEN_DURATION)*(1-sens), 0, (1/SCREEN_DURATION)*sens, 0, 0],  # CANCER_SCREENING
            [0, 0, 0, 0, 0, lambda12, 0, 0, 0, 0],  # CANCER_TREATMENT
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # CANCER_DEATH
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # OTHER_DEATH
        ]
    return rate_matrix

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
     1,  # WELL
     0,  # WELL_SCREENING
     0.9,  # PRE_CANCER
     0,  # PRE_CANCER_SCREENING
     0,  # PRE_CANCER_TREATMENT (cost of colposcopy)
     0.2,  # CANCER
     0,    # CANCER_SCREENING
     0.2,  # CANCER_TREATMENT
     0,  # CANCER_DEATH
     0,  # OTHER_DEATH
 ]

# treatment costs
HPV_SCREEN_COST = 117
CRYT_SCREEN_COST = 98
DUAL_SCREEN_COST = 142
CANCER_TREATMENT_COST = 1702
PRECANCER_TREATMENT_COST = 299
#COLPOSCOPY_COST = 299