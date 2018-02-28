import scipy
import bayesian_bootstrap.bootstrap as bootstrap


def bayes_bootstrap(observed, stat_function, replications, resample_size):
    data_bs = bootstrap.bayesian_bootstrap(
        list(filter(None, observed)), stat_function, replications, resample_size)
    return {
        'bootstrap_data': data_bs,
        'central_tendency': {
            str(stat_function.__name__): stat_function(data_bs)
        },
        'CIs': {
            'high':  scipy.stats.mstats.mquantiles(data_bs, prob=[0.975])[0],
            'low': scipy.stats.mstats.mquantiles(data_bs, prob=[0.025])[0]
        } if stat_function.__name__ == 'median' else {
            'high':  stat_function(data_bs) + (1.96 * scipy.std(data_bs)),
            'low': stat_function(data_bs) - (1.96 * scipy.std(data_bs))
        }
    }


def bayes_bootstrap_median_diffs(sample1, sample2, replications=10000):
    bs_sample1 = bayes_bootstrap(sample1, scipy.median, replications, len(sample1))['bootstrap_data']
    bs_sample2 = bayes_bootstrap(sample2, scipy.median, replications, len(sample2))['bootstrap_data']
    return _compare_bootstraped_medians(bs_sample1, bs_sample2)


def _compare_bootstraped_medians(bs_sample1, bs_sample2):
    median_diffs = [x - y for x in bs_sample1 for y in bs_sample2]
    return {
        'median_diffs': median_diffs,
        'central_tendency': scipy.median(median_diffs),
        'CIs': {
            'high':  scipy.stats.mstats.mquantiles(median_diffs, prob=[0.975])[0],
            'low': scipy.stats.mstats.mquantiles(median_diffs, prob=[0.025])[0]
        }
    }
