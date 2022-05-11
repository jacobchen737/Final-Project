import InputData as D
import MarkovModelClasses as Cls
import ParameterClasses as P
import Support as Support


# create a cohort
cohort_cryt = Cls.Cohort(id=1,
                         pop_size=D.POP_SIZE,
                         parameters=P.Parameters(treatment=D.Treatment.CRYT_SCREEN))
# simulate the cohort
cohort_cryt.simulate(sim_length=D.SIMULATION_LENGTH)

# simulating
# create a cohort
cohort_hpv = Cls.Cohort(id=2,
                        pop_size=D.POP_SIZE,
                        parameters=P.Parameters(treatment=D.Treatment.HPV_SCREEN))
# simulate the cohort
cohort_hpv.simulate(sim_length=D.SIMULATION_LENGTH)


cohort_dual = Cls.Cohort(id=3,
                         pop_size=D.POP_SIZE,
                         parameters=P.Parameters(treatment=D.Treatment.DUAL_SCREEN))

cohort_dual.simulate(sim_length=D.SIMULATION_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS

Support.print_outcomes(sim_outcomes=cohort_hpv.cohortOutcomes,
                       treatment_name=D.Treatment.HPV_SCREEN)
Support.print_outcomes(sim_outcomes=cohort_cryt.cohortOutcomes,
                       treatment_name=D.Treatment.CRYT_SCREEN)
Support.print_outcomes(sim_outcomes=cohort_dual.cohortOutcomes,
                       treatment_name=D.Treatment.DUAL_SCREEN)

# plot survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_1=cohort_hpv.cohortOutcomes,
                                            treatment1=D.Treatment.HPV_SCREEN,
                                            sim_outcomes_2=cohort_cryt.cohortOutcomes,
                                            treatment2=D.Treatment.CRYT_SCREEN)

Support.plot_survival_curves_and_histograms(sim_outcomes_1=cohort_hpv.cohortOutcomes,
                                            treatment1=D.Treatment.HPV_SCREEN,
                                            sim_outcomes_2=cohort_dual.cohortOutcomes,
                                            treatment2=D.Treatment.DUAL_SCREEN)

Support.plot_survival_curves_and_histograms(sim_outcomes_1=cohort_dual.cohortOutcomes,
                                            treatment1=D.Treatment.DUAL_SCREEN,
                                            sim_outcomes_2=cohort_cryt.cohortOutcomes,
                                            treatment2=D.Treatment.CRYT_SCREEN)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_1=cohort_hpv.cohortOutcomes,
                                   treatment1=D.Treatment.HPV_SCREEN,
                                   sim_outcomes_2=cohort_cryt.cohortOutcomes,
                                   treatment2=D.Treatment.CRYT_SCREEN)

Support.print_comparative_outcomes(sim_outcomes_1=cohort_hpv.cohortOutcomes,
                                   treatment1=D.Treatment.HPV_SCREEN,
                                   sim_outcomes_2=cohort_dual.cohortOutcomes,
                                   treatment2=D.Treatment.DUAL_SCREEN)

Support.print_comparative_outcomes(sim_outcomes_1=cohort_dual.cohortOutcomes,
                                   treatment1=D.Treatment.DUAL_SCREEN,
                                   sim_outcomes_2=cohort_cryt.cohortOutcomes,
                                   treatment2=D.Treatment.CRYT_SCREEN)


# report the CEA results
Support.report_CEA_CBA(sim_outcomes_hpv=cohort_hpv.cohortOutcomes,
                       sim_outcomes_cryt=cohort_cryt.cohortOutcomes)

