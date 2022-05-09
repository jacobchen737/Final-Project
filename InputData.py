from enum import Enum

# simulation settings
POP_SIZE = 1000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

class HealthStates(Enum):
    """ health states of patients with HIV """
    WELL = 0
    HR_HPV = 1
    L_DYSPLASIA = 2
    H_DYSPLASIA = 3
    CANCER = 4
    CANCER_DEATH = 5
    OTHER_DEATH = 6

# transition matrix
TRANS_MATRIX = [
    [0, 0, 0, 0, 0, 0, 0],   # WELL
    [0, 0, 0, 0, 0, 0, 0],   # HR_HPV
    [0, 0, 0, 0, 0, 0, 0],   # L_DYSPLASIA
    [0, 0, 0, 0, 0, 0, 0],   # H_DYSPLASIA
    [0, 0, 0, 0, 0, 0, 0],   # CANCER
    [0, 0, 0, 0, 0, 0, 0],   # CANCER_DEATH
    [0, 0, 0, 0, 0, 0, 0]   # OTHER_DEATH
    ]

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,     # WELL
    0,     # HR_HPV
    0,     # L_DYSPLASIA
    0,     # H_DYSPLASIA
    1702,  # CANCER
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
HPV_VACC_COST = 400
HPV_SCREEN_COST = 117
CRYT_SCREEN_COST = 98
DUAL_SCREEN_COST = 142
COLPOSCOPY_COST = 299

# treatment relative risk
HPV_VACC_RR = 0.83
HPV_SCREEN_RR = 0.9260
CRYT_SCREEN_RR = 0.7550
DUAL_SCREEN_RR = 0.9370