import InputData as D
import SimPy.EconEval as Econ
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
import SimPy.Statistics as Stat

def print_outcomes(multi_cohort_outcomes, therapy_name):
    survival_mean_PI_text = multi_cohort_outcomes.statMeanSurvivalTime \
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost \
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_PI_text)

    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_PI_text)

def print_comparative_outcomes(multi_cohort_outcomes_1, multi_cohort_outcomes_2):
    increase_mean_survival_time = Stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_1.meanSurvivalTimes,
        y_ref=multi_cohort_outcomes_2.meanSurvivalTimes)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean survival time and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_mean_discounted_cost = Stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_1.meanCosts,
        y_ref=multi_cohort_outcomes_2.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2,
                                                                                form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted QALY under combination therapy with respect to mono therapy
    increase_mean_discounted_qaly = Stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_cohort_outcomes_1.meanQALYs,
        y_ref=multi_cohort_outcomes_2.meanQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

def report_CEA_CBA(multi_cohort_outcomes_HPV, multi_cohort_outcomes_CRYT):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # define two strategies
    HPV_strategy = Econ.Strategy(
        name='HPV Screening',
        cost_obs=multi_cohort_outcomes_HPV.meanCosts,
        effect_obs=multi_cohort_outcomes_HPV.meanQALYs,
        color='green'
    )
    CRYT_strategy = Econ.Strategy(
        name='Crytology Screening',
        cost_obs=multi_cohort_outcomes_CRYT.meanCosts,
        effect_obs=multi_cohort_outcomes_CRYT.meanQALYs,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[HPV_strategy, CRYT_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional Discounted QALY',
        y_label='Additional Discounted Cost',
        fig_size=(6, 5),
        add_clouds=True,
        transparency=0.2)

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # uncertainty (projection) interval
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    NBA = Econ.CBA(
        strategies=[HPV_strategy, CRYT_strategy],
        wtp_range=(0, 50000),
        if_paired=True
    )
    # show the net monetary benefit figure
    NBA.plot_incremental_nmbs(
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='p',
        show_legend=True,
        figure_size=(6, 5),
    )
