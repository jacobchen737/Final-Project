import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support
import SimPy.Plots.SamplePaths as Path
import SimPy.Plots.Histogram as Hist

#select therapy
therapy = P.Treatment.HPV_SCREEN

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      Treatment=P.Treatment.HPV_SCREEN)

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=D.SIM_TIME_STEPS)

# plot the sample path (survival curve)
Path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# plot the histogram of number of cancer cases
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.nCancers,
    title='Histogram of Number of Cancer Cases',
    x_label='Number of Cancer Cases',
    y_label='Count',
    bin_width=1)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,
                       therapy_name=therapy)