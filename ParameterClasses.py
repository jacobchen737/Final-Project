from enum import Enum
import numpy as np
import InputData as Data

class Parameters:
    def __init__(self, treatment):

        # selected therapy
        self.treatment = treatment

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL
        # annual state costs and utilities

        self.annualStateCosts = Data.ANNUAL_STATE_COST_SCREENING

        # discount rate
        self.discountRate = Data.DISCOUNT

        self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=treatment)

        #  transition rate matrices
        if self.treatment == Data.Treatment.HPV_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.HPV_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.HPV_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.CANCER_SCREENING.value] = Data.HPV_SCREEN_COST

        if self.treatment == Data.Treatment.CRYT_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.CRYT_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.CRYT_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.CANCER_SCREENING.value] = Data.CRYT_SCREEN_COST

        if self.treatment == Data.Treatment.DUAL_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.DUAL_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.DUAL_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.CANCER_SCREENING.value] = Data.DUAL_SCREEN_COST

        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        self.cancerTreatmentCost = Data.CANCER_TREATMENT_COST
        self.precancerTreatmentCost = Data.PRECANCER_TREATMENT_COST