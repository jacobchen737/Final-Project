from enum import Enum

# simulation settings
POP_SIZE = 1000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

ANNUAL_PROB_BACKGROUND_MORT = 8.15 / 1000

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

# treatment sensitivity
HPV_SCREEN_RR = 0.9260
CRYT_SCREEN_RR = 0.7550
DUAL_SCREEN_RR = 0.9370

ANNUAL_PROB_BACKGROUND_MORT = 41.4/1000
ANNUAL_PROB_CERVICALCANCER_MORT = 36.2/100000
ANNUAL_PROB_FIRST_CERVICALCANCER = 15/1000
PROB_SCREEN_WELL = 0.75
PROB_SCREEN_DISEASE = 0.7
FIVE_YEAR_PROB_RECURRENT_CANCER = 0.17
SCREEN_DURATION = 1/365

# Part 1: find the annual rate of non-cervical-cancer death
annual_prob_non_cervicalcancer_mort = (ANNUAL_PROB_BACKGROUND_MORT - ANNUAL_PROB_CERVICALCANCER_MORT)
lambda0 = -np.log(1 - annual_prob_non_cervicalcancer_mort)

# Part 2: lambda 1 + lambda 2
lambda1_plus2 = -np.log(1 - ANNUAL_PROB_FIRST_CERVICALCANCER)


lambda5 = 1 / SCREEN_DURATION



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