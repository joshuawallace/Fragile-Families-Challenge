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
    """Remove rows from the data if the outcome corresponding to 
    that row is NA

    Arguments:
        data {array-like} -- the survey data
        outcomes {list-like} -- list of the outcomes

    Raises:
        RuntimeError -- The code is only able to take a 1-d outcome list
    """
    try:
        len(outcomes[0])
        raise RuntimeError("This code only capable of taking 1-D list, not 2-D list")
    except TypeError:
        pass

    data_processed, outcomes_processed = zip(*((d, o) for d, o in zip(data, outcomes) if o != 'NA'))
    return (data_processed, outcomes_processed)


def convert_NA_values_to_NaN(data, also_convert_negatives=False, deepcopy=True):
    """Convert all the NA values to NaN's so they can be imputed

    Arguments:
        data {array-like} -- the survey data

    Keyword Arguments:
        also_convert_negatives {bool} -- also convert negative values to NaN (default: {False})
        deepcopy {bool} -- deep copy the data instead of shallow copy (default: {True})

    Returns:
        array-like -- the original data, now with NaN's instead of NA's
    """
    if deepcopy:  # If deepcopy is true
        data_to_return = copy.deepcopy(data)
    else:
        data_to_return = copy.copy(data)

    # Loop over all the data elements
    for i in range(len(data_to_return)):
        for j in range(len(data_to_return[i])):
            if data_to_return[i][j] == 'NA':  # Convert all NA values to NaN's
                data_to_return[i][j] = np.nan
            # Convert also negative values to NaN's if parameter is set to be true
            elif data_to_return[i][j] < 0. and also_convert_negatives:
                data_to_return[i][j] = np.nan

    return data_to_return


def remove_columns_with_large_number_of_missing_values(data, frac_missing_to_remove, deepcopy=True, extra_tagalong=False):
    """Remove columns with a fraction greater than frac_missing_to_remove of
    either missing values or of the same value

    Arguments:
        data {array-like} -- the survey data
        frac_missing_to_remove {float} -- the fraction of the values that
            need to be NA for the column to be removed

    Keyword Arguments:
        deepcopy {bool} -- deep copy the data instead of shallow copy (default: {True})
        extra_tagalong {false or array-like} -- another array upon which to remove the same values

    Returns:
        array-like -- the original data, now with NaN's instead of NA's
    """

    columns_to_remove = []
    n = len(data)

    if deepcopy:  # Deecopy if set
        data_to_return = copy.deepcopy(data)
    else:
        data_to_return = copy.copy(data)

    # Over all the columns
    for j in range(len(data[0])):
        n_missing = 0
        for i in range(n):
            if np.isnan(data_to_return[i][j]):
                n_missing += 1  # Count how many missing values there are

        if float(n_missing)/float(n) > frac_missing_to_remove:
            columns_to_remove.append(j)  # Record columns if there is a greater than a certain fraction missing values.

    print "Removing some columns, those that have greater than a " + str(frac_missing_to_remove) + " fraction of missing values."
    print str(len(columns_to_remove)) + " columns removed, out of " + str(len(data[0])) + " total columns."

    # Remove the columns
    for j in reversed(columns_to_remove):
        for i in range(n):
            _ = data_to_return[i].pop(j)
        if extra_tagalong != False:
            for k in range(len(extra_tagalong)):
                _ = extra_tagalong[k].pop(j)

    if extra_tagalong == False:
        return data_to_return
    else:
        return (data_to_return, extra_tagalong)
