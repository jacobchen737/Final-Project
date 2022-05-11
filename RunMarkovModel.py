import InputData as D
import MarkovModelClasses as Cls
import ParameterClasses as P
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
import Support as Support

# selected therapy
treatment = D.Treatment.HPV_SCREEN

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      parameters=P.Parameters(treatment=treatment))

# simulate the cohort over the specified time steps
myCohort.simulate(sim_length=D.SIMULATION_LENGTH)

# plot the sample path (survival curve)
Path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.nTotalCancer,
    title='Histogram of Patient Total Strokes',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,treatment_name=treatment)