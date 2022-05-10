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
        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST

        # discount rate
        self.discountRate = Data.DISCOUNT

        self.transRateMatrix = []

        #  transition rate matrices
        if self.treatment == Treatment.HPV_SCREEN:
            self.transRateMatrix = Data.TRANS_MATRIX_HPV
            self.annualStateCosts[1] = Data.HPV_SCREEN_COST
            self.annualStateCosts[3] = Data.HPV_SCREEN_COST
            self.annualStateCosts[6] = Data.HPV_SCREEN_COST

        if self.treatment == Treatment.CRYT_SCREEN:
            self.transRateMatrix = Data.TRANS_MATRIX_CRYT
            self.annualStateCosts[1] = Data.CRYT_SCREEN_COST
            self.annualStateCosts[3] = Data.CRYT_SCREEN_COST
            self.annualStateCosts[6] = Data.CRYT_SCREEN_COST

        if self.treatment == Treatment.DUAL_SCREEN:
            self.transRateMatrixMatrix = Data.TRANS_MATRIX_DUAL
            self.annualStateCosts[1] = Data.DUAL_SCREEN_COST
            self.annualStateCosts[3] = Data.DUAL_SCREEN_COST
            self.annualStateCosts[6] = Data.DUAL_SCREEN_COST