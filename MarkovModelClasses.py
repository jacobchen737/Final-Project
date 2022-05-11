import numpy as np

import SimPy.EconEval as Econ
import SimPy.Markov as Markov
import SimPy.SamplePath as Path
import SimPy.Statistics as Stat
from InputData import HealthStates


class Patient:
    def __init__(self, id, parameters):

        self.id = id
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, sim_length):

        # random number generator for this patient
        rng = np.random.RandomState(seed=self.id)
        # gillespie algorithm
        gillespie = Markov.Gillespie(transition_rate_matrix=self.params.transRateMatrix)

        t = 0  # simulation time
        if_stop = False

        while not if_stop:
            # find time until next event (dt), and next state
            # (note that the gillespie algorithm returns None for dt if the process
            # is in an absorbing state)
            dt, new_state_index = gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # stop if time to next event (dt) is None (i.e. we have reached an absorbing state)
            if dt is None:
                if_stop = True

            else:
                # else if next event occurs beyond simulation length
                if dt + t > sim_length:
                    # advance time to the end of the simulation and stop
                    t = sim_length
                    # the individual stays in the current state until the end of the simulation
                    new_state_index = self.stateMonitor.currentState.value
                    if_stop = True
                else:
                    # advance time to the time of next event
                    t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthStates(new_state_index))


class PatientStateMonitor:
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nCancer = 0
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, new_state):

        if new_state in (HealthStates.CANCER_DEATH, HealthStates.OTHER_DEATH):
            self.survivalTime = time

        if new_state == HealthStates.CANCER:
            self.nCancer += 1

        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState,
                                       next_state=new_state)

        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState in (HealthStates.CANCER_DEATH, HealthStates.OTHER_DEATH):
            return False
        else:
            return True


class PatientCostUtilityMonitor:
    def __init__(self, parameters):

        self.tLastRecorded = 0  # time when the last cost and outcomes got recorded

        self.params = parameters
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, time, current_state, next_state):

        # cost (per unit of time) during the period since the last recording until now
        cost = self.params.annualStateCosts[current_state.value]
        if current_state == HealthStates.CANCER_TREATMENT:
            cost += self.params.cancerTreatmentCost
        if current_state == HealthStates.PRE_CANCER_TREATMENT:
            cost += self.params.precancerTreatmentCost

        # discounted cost and utility (continuously compounded)
        discounted_cost = Econ.pv_continuous_payment(payment=cost,
                                                     discount_rate=self.params.discountRate,
                                                     discount_period=(self.tLastRecorded, time))



        # utility (per unit of time) during the period since the last recording until now
        utility = self.params.annualStateUtilities[current_state.value]
        discounted_utility = Econ.pv_continuous_payment(payment=utility,
                                                        discount_rate=self.params.discountRate,
                                                        discount_period=(self.tLastRecorded, time))

        # update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        self.totalDiscountedUtility += discounted_utility

        # update the time since last recording to the current time
        self.tLastRecorded = time


class Cohort:
    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param parameters: parameters
        """
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params)
            # simulate
            patient.simulate(sim_length)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):
        self.statNumCancer = None
        self.survivalTimes = []
        self.nTotalCancer = []
        self.nLivingPatients = None
        self.costs = []
        self.utilities = []
        self.statSurvivalTime = None
        self.statCost = None
        self.statUtility = None

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record survival time
        if not (simulated_patient.stateMonitor.survivalTime is None):
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        self.nTotalCancer.append(simulated_patient.stateMonitor.nCancer)
        self.costs.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
        self.utilities.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # summary statistics
        self.statNumCancer = Stat.SummaryStat(name='Number of strokes', data=self.nTotalCancer)
        self.statSurvivalTime = Stat.SummaryStat(name='Survival Time', data=self.survivalTimes)
        self.statCost = Stat.SummaryStat(name='Discounted Cost', data=self.costs)
        self.statUtility = Stat.SummaryStat(name='Discounted Utility', data=self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1] * len(self.survivalTimes)
        )
