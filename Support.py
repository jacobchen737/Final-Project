import InputData as D
import SimPy.EconEval as Econ
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
import SimPy.Statistics as Stat

def print_outcomes(sim_outcomes, treatment_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTime.get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # print outcomes
    print(treatment_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_CI_text)

    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def plot_survival_curves_and_histograms(sim_outcomes_1, treatment1, sim_outcomes_2, treatment2):
    """ draws the survival curves and the histograms of time until HIV deaths
    :param sim_outcomes_hpv: outcomes of a cohort simulated under hpv therapy
    :param sim_outcomes_: outcomes of a cohort simulated under cryt therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_1.nLivingPatients,
        sim_outcomes_2.nLivingPatients
    ]
    if treatment1 == D.Treatment.CRYT_SCREEN:
        color1 = 'green'
    if treatment1 == D.Treatment.HPV_SCREEN:
        color1 = 'blue'
    if treatment1 == D.Treatment.DUAL_SCREEN:
        color1 = 'red'
    if treatment2 == D.Treatment.CRYT_SCREEN:
        color2 = 'green'
    if treatment2 == D.Treatment.HPV_SCREEN:
        color2 = 'blue'
    if treatment2 == D.Treatment.DUAL_SCREEN:
        color2 = 'red'
    # graph survival curve
    Path.plot_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=[treatment1, treatment2],
        color_codes=[color1, color2]
    )
# histograms of cancer times
    set_of_cancer = [
        sim_outcomes_1.nTotalCancer,
        sim_outcomes_2.nTotalCancer
    ]

    # graph histograms
    Hist.plot_histograms(
        data_sets=set_of_cancer,
        title='Histogram of patient cancer number',
        x_label='Number of Cancer',
        y_label='Counts',
        bin_width=1,
        legends=[treatment1, treatment2],
        color_codes=[color1, color2],
        transparency=0.6
    )

def print_comparative_outcomes(sim_outcomes_1,
                               treatment1,
                               sim_outcomes_2,
                               treatment2):

    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """
    print("Compare ",
          treatment1,
          " vs ",
          treatment2)

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_1.survivalTimes,
        y_ref=sim_outcomes_2.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(interval_type='c',
                                                                         alpha=D.ALPHA,
                                                                         deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_1.costs,
        y_ref=sim_outcomes_2.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(interval_type='c',
                                                                           alpha=D.ALPHA,
                                                                           deci=2,
                                                                           form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted utility under combination therapy with respect to mono therapy

    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_1.utilities,
        y_ref=sim_outcomes_2.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(interval_type='c',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)

    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

def report_CEA_CBA(sim_outcomes_hpv, sim_outcomes_cryt):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # define two strategies
    hpv_therapy_strategy = Econ.Strategy(
        name='With HPV Screening ',
        cost_obs=sim_outcomes_hpv.costs,
        effect_obs=sim_outcomes_hpv.utilities,
        color='green'
    )
    cryt_therapy_strategy = Econ.Strategy(
        name='With CRYT Screening',
        cost_obs=sim_outcomes_cryt.costs,
        effect_obs=sim_outcomes_cryt.utilities,
        color='blue'
    )
    # do CEA
    CEA = Econ.CEA(
        strategies=[hpv_therapy_strategy, cryt_therapy_strategy],
        if_paired=False
    )

    # plot cost-effectiveness figure
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional QALYs',
        y_label='Additional Cost',
        x_range=(0,10),
        y_range=(10, 2000)
    )


    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    NBA = Econ.CBA(
        strategies=[hpv_therapy_strategy, cryt_therapy_strategy],
        wtp_range=[0, 5000],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.plot_incremental_nmbs(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5)
    )
