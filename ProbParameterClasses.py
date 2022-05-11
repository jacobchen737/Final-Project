import SimPy.RandomVariateGenerators as RVGs
from ParameterClasses import *

class Parameters:
    def __init__(self, treatment):

        self.annualStateCosts = []

        # selected therapy
        self.treatment = treatment

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL
        # annual state costs and utilities

        self.annualStateCosts = Data.ANNUAL_STATE_COST_SCREENING

        # discount rate
        self.discountRate = Data.DISCOUNT


        #  transition rate matrices
        if self.treatment == Data.Treatment.HPV_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.HPV_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.HPV_SCREEN_COST

        if self.treatment == Data.Treatment.CRYT_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.CRYT_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.CRYT_SCREEN_COST

        if self.treatment == Data.Treatment.DUAL_SCREEN:
            self.annualStateCosts[Data.HealthStates.WELL_SCREENING.value] = Data.DUAL_SCREEN_COST
            self.annualStateCosts[Data.HealthStates.PRE_CANCER_SCREENING.value] = Data.DUAL_SCREEN_COST

        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        self.cancerTreatmentCost = Data.CANCER_TREATMENT_COST
        self.precancerTreatmentCost = Data.PRECANCER_TREATMENT_COST

        self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=treatment)
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        self.cancerTreatmentCost = Data.CANCER_TREATMENT_COST
        self.precancerTreatmentCost = Data.PRECANCER_TREATMENT_COST

class ParameterGenerator:
    def __init__(self, treatment):

        self.treatment = treatment
        self.annualStateCostRVG = []

        for cost in Data.ANNUAL_STATE_COST_SCREENING:
            if cost == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                fit_output = RVGs.Gamma.fit_mm(mean=cost,st_dev=cost / 5)
                self.annualStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                           loc=0,
                           scale=fit_output["scale"]))

        if self.treatment == Data.Treatment.HPV_SCREEN:
            treatment_cost = Data.HPV_SCREEN_COST
        elif self.treatment == Data.Treatment.CRYT_SCREEN:
            treatment_cost = Data.CRYT_SCREEN_COST
        elif self.treatment == Data.Treatment.DUAL_SCREEN:
            treatment_cost = Data.DUAL_SCREEN_COST

        fit_output = RVGs.Gamma.fit_mm(mean=treatment_cost,st_dev=treatment_cost/5)

        self.annualStateCostRVG[Data.HealthStates.WELL_SCREENING.value] = RVGs.Gamma(a=fit_output["a"],
                                                                                     loc=0,
                                                                                     scale=fit_output["scale"])
        self.annualStateCostRVG[Data.HealthStates.PRE_CANCER_SCREENING.value] = RVGs.Gamma(a=fit_output["a"],
                                                                                     loc=0,                                                                       scale=fit_output["scale"])

        self.annualStateCostRVG[Data.HealthStates.CANCER_SCREENING.value] = RVGs.Gamma(a=fit_output["a"],
                                                                                     loc=0,
                                                                                     scale=fit_output["scale"])
    def get_new_parameters(self, rng):
            """
            :param rng: random number generator
            :return: a new parameter set
            """

            # create a parameter set
            param = Parameters(treatment=self.treatment)

            for dist in self.annualStateCostRVG:
                param.annualStateCosts.append(dist.sample(rng))

            return param
