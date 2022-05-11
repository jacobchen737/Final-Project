from enum import Enum
import numpy as np

# simulation settings
POP_SIZE = 1000         # cohort population size
SIMULATION_LENGTH = 50    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
class Treatment(Enum):
    HPV_SCREEN = 0
    CRYT_SCREEN = 1
    DUAL_SCREEN = 2

class HealthStates(Enum):
    WELL = 0
    WELL_SCREENING = 1
    PRE_CANCER = 2
    PRE_CANCER_SCREENING = 3
    PRE_CANCER_TREATMENT = 4
    CANCER = 5
    CANCER_TREATMENT = 6
    CANCER_DEATH = 7
    OTHER_DEATH = 8

# treatment sensisitivy
HPV_SCREEN_RR = 0.9260
CRYT_SCREEN_RR = 0.75
DUAL_SCREEN_RR = 0.9370


# annual cost of each health state
ANNUAL_STATE_COST_SCREENING = [
    0,     # WELL
    0,     # WELL_SCREENING
    100,     # PRE_CANCER
    0,     # PRE_CANCER_SCREENING
    0,   # PRE_CANCER_TREATMENT (cost of colposcopy)
    1000,     # CANCER
    0,  # CANCER_TREATMENT
    0,     # CANCER_DEATH
    0,     # OTHER_DEATH
    ]




ANNUAL_PROB_ALL_CAUSE_MORT = 41.4 / 1000
ANNUAL_PROB_CERVICALCANCER_MORT = 311000 / 3904727342
PROB_WELL_PRECANCER = 0.10636
PROB_WELL_CANCER = 0.007
PROB_WELL_WELL = 1-PROB_WELL_CANCER-PROB_WELL_PRECANCER
PROB_PRECANCER_WELL = 0.6
PROB_PRECANCER_CANCER = 0.4
PROB_CANCER_DEATH = 0.361753675

SCREEN_DURATION = 1/365  # 1 day
PRECANCERTREATMENT_DURATION = 1/4
CANCERTREATMENT_DURATION = 1/2

HPV_SCREEN_FREQUENCY = 1/5
CRYT_SCREEN_FREQUENCY = 1/3
DUAL_SCREEN_FREQUENCY = 1/5
NO_SCREEN_FREQUENCY = 1/3




def get_trans_rate_matrix(with_treatment):
    """
    :param with_treatment:  to calculate the transition rate matrix when the anticoagulation is used

    :return: transition rate matrix
    """
    #  WELL->WELLSCREENING  PRECANCER->PRECANCERSCREEN
    if with_treatment == Treatment.HPV_SCREEN:
        lambda13 = 1 / HPV_SCREEN_FREQUENCY
        rr = 1-HPV_SCREEN_RR

    if with_treatment == Treatment.CRYT_SCREEN:
        lambda13 = 1 / CRYT_SCREEN_FREQUENCY
        rr = 1-CRYT_SCREEN_RR

    if with_treatment == Treatment.DUAL_SCREEN:
        lambda13 = 1 / DUAL_SCREEN_FREQUENCY
        rr = 1-DUAL_SCREEN_RR



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
    lambda5 = -np.log(1 - PROB_CANCER_DEATH)

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


    rate_matrix = [
    [0, lambda13, lambda1, 0, 0, lambda2, 0, 0, lambda0],  # WELL
    [lambda9/rr, 0, 0, 0, lambda6*rr, 0, lambda7*rr, 0, lambda0*(1/SCREEN_DURATION)*rr],  # WELL_SCREENING
    [0, 0, 0, 0, lambda13, lambda4, 0, 0, lambda0],  # PRE_CANCER
    [0, 0, 0, 0, lambda11/rr, 0, lambda10*rr, 0, lambda0*(1/SCREEN_DURATION)*rr],  # PRE_CANCER_SCREENING
    [lambda3, 0, 0, 0, 0, 0, 0, 0, lambda0*(1/PRECANCERTREATMENT_DURATION)],  # PRE_CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, lambda5, 0],  # CANCER
    [0, 0, 0, 0, 0, lambda12, 0, 0, 0],  # CANCER_TREATMENT
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # CANCER_DEATH
    [0, 0, 0, 0, 0, 0, 0, 0, 0]  # OTHER_DEATH
    ]
    return rate_matrix





# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
     1,  # WELL
     1,  # WELL_SCREENING
     0.6,  # PRE_CANCER
     0.6,  # PRE_CANCER_SCREENING
     0.5,  # PRE_CANCER_TREATMENT (cost of colposcopy)
     0.1,  # CANCER
     0.1,  # CANCER_TREATMENT
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