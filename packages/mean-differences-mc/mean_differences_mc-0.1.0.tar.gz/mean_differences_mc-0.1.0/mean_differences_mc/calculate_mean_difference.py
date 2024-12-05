import numpy as np
from .switch_elements import switch_elements
from .index_switch import index_to_switch


def calculate_mean_difference(minuend, subtrahend):
    mean_minuend = np.mean(minuend)
    mean_subtrahend = np.mean(subtrahend)
    mean_diference = mean_minuend - mean_subtrahend
    return mean_diference


def calculate_mean_switched_difference(minuend, subtrahend, n_switches):
    max_lim = len(minuend) - 1
    minuend_switched = np.copy(minuend)
    subtrahend_switched = np.copy(subtrahend)
    mean_switched_difference = []
    for _ in range(n_switches):
        index_test = index_to_switch(max_lim)
        minuend_switched, subtrahend_switched = switch_elements(
            minuend_switched, subtrahend_switched, index_test
        )
        mean_defference = calculate_mean_difference(minuend_switched, subtrahend_switched)
        mean_switched_difference.append(mean_defference)
    return mean_switched_difference


def calculate_p_value_from_difference(difference, difference_array):
    mask = np.array(difference_array) >= difference
    significant_diferences = np.sum([mask])
    return significant_diferences / len(difference_array)
