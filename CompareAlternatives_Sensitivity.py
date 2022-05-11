import InputData as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import ProbParameterClasses as P

N_COHORTS = 200  # number of cohorts
POP_SIZE = 100 # population size of each cohort

# create a multi-cohort to simulate under mono therapy
multiCohortHPV = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    treatment=D.Treatment.HPV_SCREEN
)

multiCohortHPV.simulate(sim_length=D.SIMULATION_LENGTH)

# create a multi-cohort to simulate under combo therapy
multiCohortCRYT = Cls.MultiCohort(
    ids=range(N_COHORTS, 2*N_COHORTS),
    pop_size=POP_SIZE,
    treatment=D.Treatment.CRYT_SCREEN
)

multiCohortCRYT.simulate(sim_length=D.SIMULATION_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohortHPV.multiCohortOutcomes,
                       therapy_name=D.Treatment.HPV_SCREEN)
Support.print_outcomes(multi_cohort_outcomes=multiCohortCRYT.multiCohortOutcomes,
                       therapy_name=D.Treatment.CRYT_SCREEN)


# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_1=multiCohortHPV.multiCohortOutcomes,
                                   multi_cohort_outcomes_2=multiCohortCRYT.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_HPV=multiCohortHPV.multiCohortOutcomes,
                       multi_cohort_outcomes_CRYT=multiCohortCRYT.multiCohortOutcomes)