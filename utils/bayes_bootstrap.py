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