from enum import Enum
import numpy as np
import InputData as Data

class Treatment(Enum):
    """ mono vs. combination therapy """
    VACCINE = 0
    HPV_SCREEN = 1
    CRYT_SCREEN = 2
    DUAL_SCREEN = 3

class Parameters:
    def __init__(self, treatment, time):

        # selected therapy
        self.treatment = treatment
        self.time = time

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL
        self.probMatrix = []

        #  treatment costs & probability matrices
        if self.treatment == Treatment.HPV_SCREEN:
            if time % 5 == 0:
                self.treatmentCost = Data.HPV_SCREEN_COST
                self.probMatrix = Data.TRANS_MATRIX_HPV
            else:
                self.treatmentCost = 0
                self.probMatrix = Data.TRANS_MATRIX_NONE

        if self.treatment == Treatment.CRYT_SCREEN:
            if time % 3 == 0:
                self.treatmentCost = Data.CRYT_SCREEN_COST
                self.probMatrix = Data.TRANS_MATRIX_CRYT
            else:
                self.treatmentCost = 0
                self.probMatrix = Data.TRANS_MATRIX_NONE

        if self.treatment == Treatment.DUAL_SCREEN:
            if time % 5 == 0:
                self.treatmentCost = Data.DUAL_SCREEN_COST
                self.probMatrix = Data.TRANS_MATRIX_DUAL
            else:
                self.treatmentCost = 0
                self.probMatrix = Data.TRANS_MATRIX_NONE

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST

        # discount rate
        self.discountRate = Data.DISCOUNT