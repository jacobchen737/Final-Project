from enum import Enum

# simulation settings
POP_SIZE = 1000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate


class HealthStates(Enum):
    """ health states of patients with HIV """
    CD4_200to500 = 0
    CD4_200 = 1
    AIDS = 2
    HIV_DEATH = 3


# transition matrix
TRANS_MATRIX = [
    [1251,  350,    116,    17],   # CD4_200to500
    [0,     731,    512,    15],   # CD4_200
    [0,     0,      1312,   437]   # AIDS
    ]

# annual cost of each health state
ANNUAL_STATE_COST = [
    2756.0,     # CD4_200to500
    3025.0,     # CD4_200
    9007.0,     # AIDS
    0,          # Dead
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    0.75,   # CD4_200to500
    0.50,   # CD4_200
    0.25,   # AIDS
    0,      # Dead
    ]

# annual drug costs
Zidovudine_COST = 2278.0
Lamivudine_COST = 2086.0

# treatment relative risk
TREATMENT_RR = 0.509


