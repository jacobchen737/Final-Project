import numpy as np
import SimPy.Markov as Markov
import SimPy.Plots.SamplePaths as Path
from InputData import HealthStates
import SimPy.EconEval as Econ
import SimPy.Statistics as Stat

class Patient:
    def __init__(self, id, treatment):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: an instance of the parameters class
        """
        self.id = id
        self.treatment = treatment
        self.stateMonitor = PatientStateMonitor(treatment=treatment)

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        k = 0

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # jump process
        markov_jump = Markov.MarkovJumpProcess(transition_prob_matrix=self.params.probMatrix)

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:
            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1

class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, treatment):

        self.currentState = parameters.initialHealthState   # initial health state
        self.survivalTime = None      # survival time
        self.timeToCancer = None        # time to develop AIDS
        # patient's cost and utility monitor
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # update survival time
        if new_state == HealthStates.CANCER_DEATH or new_state == HealthStates.OTHER_DEATH:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update time until AIDS
        if self.currentState != HealthStates.CANCER and new_state == HealthStates.CANCER:
            self.timeToCancer = time_step + 0.5  # corrected for the half-cycle effect

        # update cost and utility
        self.costUtilityMonitor.update(k=time_step,
                                       current_state=self.currentState,
                                       next_state=new_state)

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != HealthStates.CANCER_DEATH and self.currentState != HealthStates.OTHER_DEATH:
            return True
        else:
            return False

class PatientCostUtilityMonitor:

    def __init__(self, parameters, treatment):

        # model parameters for this patient
        self.params = parameters
        self.treatment = treatment
        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param k: simulation time step
        :param current_state: current health state
        :param next_state: next health state
        """

        # update cost
        cost = 0.5 * (self.params.annualStateCosts[current_state.value] +
                      self.params.annualStateCosts[next_state.value])

        # update utility
        # utility = 0.5 * (self.params.annualStateUtilities[current_state.value] +
        #                  self.params.annualStateUtilities[next_state.value])

        # add the cost of treatment
        cost += self.params.treatmentCost

        # if death will occur, add the cost for half-year of treatment
        if next_state == HealthStates.CANCER_DEATH or next_state == HealthStates.OTHER_DEATH:
            cost += 0.5 * self.params.annualTreatmentCost
        else:
            cost += 1 * self.params.annualTreatmentCost

        # update total discounted cost and utility (corrected for the half-cycle effect)
        self.totalDiscountedCost += Econ.pv_single_payment(payment=cost,
                                                           discount_rate=self.params.discountRate / 2,
                                                           discount_period=2 * k + 1)
        self.totalDiscountedUtility += Econ.pv_single_payment(payment=utility,
                                                              discount_rate=self.params.discountRate / 2,
                                                              discount_period=2 * k + 1)

class Cohort:
    def __init__(self, id, pop_size, treatment):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param parameters: parameters
        """
        self.id = id
        self.popSize = pop_size
        self.treatment = treatment
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """

        # populate the cohort
        patients = []  # list of patients
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              treatment=self.treatment)
            # add the patient to the cohort
            patients.append(patient)

        # simulate all patients
        for patient in patients:
            # simulate
            patient.simulate(n_time_steps=n_time_steps)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(simulated_patients=patients)

class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.timesToAIDS = []           # patients' times to AIDS
        self.costs = []                 # patients' discounted costs
        self.utilities = []              # patients' discounted utilities
        self.nLivingPatients = None  # survival curve (sample path of number of alive patients over time)

        self.statSurvivalTime = None    # summary statistics for survival time
        self.statTimeToAIDS = None      # summary statistics for time to AIDS
        self.statCost = None            # summary statistics for discounted cost
        self.statUtility = None         # summary statistics for discounted utility

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        # record patient outcomes
        for patient in simulated_patients:
            # survival time
            if patient.stateMonitor.survivalTime is not None:
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            # time until AIDS
            if patient.stateMonitor.timeToAIDS is not None:
                self.timesToAIDS.append(patient.stateMonitor.timeToAIDS)
            # discounted cost and discounted utility
            self.costs.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
            self.utilities.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

        # summary statistics
        self.statSurvivalTime = Stat.SummaryStat(
            name='Survival time', data=self.survivalTimes)
        self.statTimeToAIDS = Stat.SummaryStat(
            name='Time until AIDS', data=self.timesToAIDS)
        self.statCost = Stat.SummaryStat(
            name='Discounted cost', data=self.costs)
        self.statUtility = Stat.SummaryStat(
            name='Discounted utility', data=self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )