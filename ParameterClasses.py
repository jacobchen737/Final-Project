from enum import Enum
import numpy as np
import InputData as Data

class Treatment(Enum):
    """ mono vs. combination therapy """
    HPV_SCREEN = 0
    CRYT_SCREEN = 1
    DUAL_SCREEN = 2

class Parameters:
    def __init__(self, treatment):

        # selected therapy
        self.treatment = treatment

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL
        self.transRateMatrix = []

        #  transition rate matrices
        if self.treatment == Treatment.HPV_SCREEN:
            self.transRateMatrix = Data.TRANS_MATRIX_HPV

        if self.treatment == Treatment.CRYT_SCREEN:
            self.transRateMatrix = Data.TRANS_MATRIX_CRYT

        if self.treatment == Treatment.DUAL_SCREEN:
            self.transRateMatrixMatrix = Data.TRANS_MATRIX_DUAL

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST

        # discount rate
        self.discountRate = Data.DISCOUNT