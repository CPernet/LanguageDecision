"""
Signal detection theory functions
Based on "Signal Detection theory: A user's guide"
by N.A. Macmillan and C.D. Creelman
"""
from numpy import multiply as multiply_array
from numpy import divide as divide_array
from math import exp
from scipy.stats import norm


def signal_detection(n_stim1, n_stim2, hits, false_alarms):
    misses = n_stim1 - hits
    correct_rejections = n_stim2 - false_alarms

    # Calculate p(H)
    p_hits = _p_event(hits, n_stim1)

    # Calculate p(F)
    p_false = _p_event(false_alarms, n_stim2)

    # Calculate the z values for p(H) and p(F)
    # Scipy's ppf function returns the inverse of the CDF
    # (equivalent to matlab's norminv)
    # It assumes a "standard" normal distribution by default
    # (i.e mean=0 and stddev=1)
    z_hits = norm.ppf(p_hits)
    z_false = norm.ppf(p_false)

    # Calculate the d'
    d_prime = z_hits - z_false

    # Calculate the criterion location
    c_loc = multiply_array((-1 / 2), (z_hits + z_false))

    # Calculate the relative c
    c_prime = divide_array(c_loc, d_prime)

    # Calculate the likelihood ratio beta
    beta = exp(multiply_array(c_loc, d_prime))

    # Return dictionary of results
    return{
        'z_hits': z_hits,
        'z_false': z_false,
        'd_prime': d_prime,
        'c': c_loc,
        'c_prime': c_prime,
        'beta': beta,
        'misses': misses,
        'correct_rejections': correct_rejections
    }


def _p_event(event, trials):
    """
    Return the probability of observing an event in a given
    sample space
    """
    if (event / trials) == 1:
        return 1 - (1 / (2 * trials))
    elif event == 0:
        return 1 / (2 * trials)
    return event / trials
