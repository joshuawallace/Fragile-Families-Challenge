########################
# Created 3-22-17 by JJW
# Some functions for the Fragile Families Challenge,
# this particular set of functions are designated "post-process"
# functions, i.e., functions that are run on the data after
# read in and processed by
# general_functions.check_if_data_exists_if_not_open_and_read().
# This allows for flexibility in what one chooses to do with the data
# before fitting a model to it (i.e., ignore the quantified negative values
# or not)
#
#
########################


import copy
import numpy as np


def remove_NA_from_outcomes_and_data(data, outcomes):
    try:
        len(outcomes[0])
        raise RuntimeError("This code only capable of taking 1-D list, not 2-D list")
    except TypeError:
        pass

    data_processed, outcomes_processed = zip(*((d, o) for d, o in zip(data, outcomes) if o != 'NA'))
    return (data_processed, outcomes_processed)


def convert_NA_values_to_NaN(data, also_convert_negatives=False, deepcopy=True):
    if deepcopy:
        data_to_return = copy.deepcopy(data)
    else:
        data_to_return = copy.copy(data)
    for i in range(len(data_to_return)):
        for j in range(len(data_to_return[i])):
            if data_to_return[i][j] == 'NA':
                data_to_return[i][j] = np.nan
            elif data_to_return[i][j] < 0. and also_convert_negatives:
                data_to_return[i][j] = np.nan

    return data_to_return
