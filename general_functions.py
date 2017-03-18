########################
# Created 3-8-17 by JJW
# Some general use functions for the Fragile Families Challenge
#
#
########################

import pickle
import numpy as np
import pandas as pd
import os.path


# A dict to reference outcomes by their index in the data read in
outcome_indices = {'ID': 0, 'gpa': 1, 'grit': 2, 'materialhardship': 3,
                   'eviction': 4, 'layoff': 5, 'jobtraining': 6}


def read_in_data(path, id_number_prepended_with_zeroes=False,
                 care_about_mothid1=False):
    """A function to read in the Fragile Families Challenge data

    This function reads in the appropriate .csv file, specified by
    the input variable `path`, and returns an array of the data

    Arguments:
        path {string} -- the path to the input file

    Returns:
         {np.array} -- the data in a 2-D numpy array
    """

    the_data_readin = []
    the_data = []
    with open(path, 'r') as f:
        the_data_readin = f.readlines()

    second_column_is_mothid1 = False
    if 'background.csv' in path:
        second_column_is_mothid1 = True

    for line in the_data_readin:
        if second_column_is_mothid1:
            the_data.append(line.split(',')[2:])
        else:
            the_data.append(line.split(','))

    # Remove the header line, save it as its own thing
    header = the_data.pop(0)

    if 'train.csv' in path:
        lower_bound = lambda x: 1; upper_bound = lambda y: len(y)
    elif 'background.csv' in path:
        lower_bound = lambda x: 0; upper_bound = lambda y: len(y) - 1
    else:
        raise RuntimeError("Do not understand which file type is being passed, \
          and thus do not understand which bounds to use in float conversion.")

    # Now, convert numerical values to actual numbers, instead of strings
    for i in range(len(the_data)):
        the_data[i][-1] = the_data[i][-1].strip('\n')
        for j in range(lower_bound(the_data[i]), upper_bound(the_data[i])):
            try:
                temp = float(the_data[i][j])
                the_data[i][j] = temp  # Try to convert to float
            except ValueError:  # Can't convert to float
                pass  # Do nothing, leave value be

    """if 'background.csv' in path:
        #print header[6150:6170]
        i = header.index('"cf4fint"')
        print "The time bug is at column " + str(i)
        for line in the_data:
            #Thanks to TA for the following line to fix time bug
            line[i] = ((pd.to_datetime(line[i]) - pd.to_datetime('1/1/60')) / np.timedelta64(1, 'D'))
            print ((pd.to_datetime(line[i]) - pd.to_datetime('1/1/60')) / np.timedelta64(1, 'D'))"""

    """if 'background.csv' in path:
        columns_to_remove = np.loadtxt("columns_to_remove.txt", dtype=int)
        print "Deleting " + str(len(columns_to_remove)) + " columns from " +\
            "the survey data, because all the data in those columns either " +\
            "are NA, are the same value, or the columns correspond to " +\
            "or father ID numbers."
        for line in the_data:
            for j in range(len(columns_to_remove)):
                del line[columns_to_remove[j]]
        for i in range(len(columns_to_remove)):
            del header[columns_to_remove[i]]"""

    return (header, the_data)


def remove_lines_with_all_NA(outcomes_data):
    """Removes lines from the training outcomes that have
    all NA values.  Since we don't know what outcomes the data
    have, no use training on these guys.

    Arguments:
        outcomes_data {list of lists} -- contains the training outcomes to be processed

    Returns:
        list of lists -- the original argument but with all lines containing nothing but NA's removed

    Raises:
        RuntimeError -- for some reason one of the internal lists didn't match the length of the input list.
    """

    all_NA = []  # A list that will be filled with Boolean values,
                 # specifying whether all the outcomes are NA or not.
    for i in range(len(outcomes_data)):  # Loop through the data
        # If all six outcomes are 'NA',  append True to all_NA
        try:
            true1 = 'NA' in outcomes_data[i][outcome_indices['gpa']]
            true2 = 'NA' in outcomes_data[i][outcome_indices['grit']]
            true3 = 'NA' in outcomes_data[i][outcome_indices['materialhardship']]
            true4 = 'NA' in outcomes_data[i][outcome_indices['eviction']]
            true5 = 'NA' in outcomes_data[i][outcome_indices['layoff']]
            true6 = 'NA' in outcomes_data[i][outcome_indices['jobtraining']]

            if true1 and true2 and true3 and true4 and true5 and true6:
                all_NA.append(True)
            else:  # Else append False
                all_NA.append(False)
        except TypeError:
            all_NA.append(False)

    # Checking that all_NA is the appropriate length
    if len(outcomes_data) != len(all_NA):
        raise RuntimeError("For some reason, all_NA is not the proper length \
                (the same length as the input)")

    # Form the new list based on the elements of the old list that aren't all NA
    outcomes_data_removed = [list(outcomes_data[i]) for i in range(len(outcomes_data)) if all_NA[i] == False]

    # Print out, letting you know how many rows are kept.
    print str(len(outcomes_data_removed)) + " rows kept from the training outcomes \
          out of " + str(len(outcomes_data))

    # Return
    return outcomes_data_removed


def match_up_data_with_training_set_of_outcomes(survey_data,
                                                training_outcomes_data,
                                                clean_up_training=False):

    training_data_ids = []
    for i in range(len(training_outcomes_data)):
        training_data_ids.append(training_outcomes_data[i][
                                                outcome_indices['ID']])

    survey_data_to_return_temp = [list(survey_data[i]) for i in range(len(survey_data)) if
                             survey_data[i][-1] in training_data_ids]

    # Thanks to http://jakzaprogramowac.pl/pytanie/20037,python-how-to-order-a-list-based-on-another-list for the following
    data_order = dict(zip(training_data_ids, range(len(training_data_ids))))
    survey_data_to_return = sorted(survey_data_to_return_temp, key=lambda x: data_order.get(x[-1], len(data_order)))

    missing_matches = []

    survey_data_to_return_ids = [item[-1] for item in survey_data_to_return]

    for i in range(len(training_data_ids)):
        if training_data_ids[i] not in survey_data_to_return_ids:
            missing_matches.append(training_data_ids[i])

    if missing_matches:
        print "************************"
        print "There were some id's in the training set of outcomes not in " +\
              "the survey question data.  Specifically, " + \
              str(len(missing_matches)) + " id's."

    if clean_up_training == False or not missing_matches:
        if missing_matches:
            print "Doing nothing about the missing data..."
        else:
            print "Training data cleanup is set to False"
        training_data_to_return = [list(line) for line in training_outcomes_data]

    else:
        "Matching the training outcomes to the survey data"
        training_data_to_return = [list(line) for line in training_outcomes_data]
        missing_matches.sort(reverse="true")
        for i in missing_matches:
            training_data_to_return.pop(i)

    return (survey_data_to_return, training_data_to_return)


def data_open_and_process(data_filename="background.csv",
                          training_outcomes_filename="train.csv"):

    print "Reading in training outcomes"
    training_outcomes_header, training_outcomes = read_in_data(training_outcomes_filename)
    print "Done reading in the training outcomes, now reading in survey data."

    survey_data_header, survey_data = read_in_data(data_filename)
    print "Done reading in survey data, now cleaning up training " +\
          "outcomes with all NA's."

    outcomes_NAall_removed = remove_lines_with_all_NA(training_outcomes)

    print "Now matching the survey data with the training outcomes, " +\
          "to get a training data set."
    survey_data_matched, training_outcomes_matched = \
        match_up_data_with_training_set_of_outcomes(survey_data,
                                                    outcomes_NAall_removed,
                                                    clean_up_training=True)

    print "Now removing the id numbers from the data, so the data can be " +\
          "used as is."

    _ = survey_data_header.pop(-1)
    _ = training_outcomes_header.pop(0)
    survey_data_ids = [line.pop(-1) for line in survey_data]
    survey_data_matched_to_outcomes_ids = [line.pop(-1) for line in survey_data_matched]
    training_outcomes_ids = [line.pop(0) for line in training_outcomes]
    training_outcomes_NAall_removed_ids = [line.pop(0) for line in outcomes_NAall_removed]
    training_outcomes_matched_to_outcomes_ids = [line.pop(0) for line in training_outcomes_matched]

    print "Done with input and processing."
    return {'survey_data_header': survey_data_header,
            #'survey_data': survey_data,
            #'suvey_data_ids': survey_data_ids,
            'survey_data_matched_to_outcomes': survey_data_matched,
            'survey_data_matched_to_outcomes_ids': survey_data_matched_to_outcomes_ids,
            'training_outcomes_header': training_outcomes_header,
            #'training_outcomes': training_outcomes,
            #'training_outcomes_ids': training_outcomes_ids,
            #'training_outcomes_NAall_removed': outcomes_NAall_removed,
            #'training_outcomes_NAall_removed_ids': training_outcomes_NAall_removed_ids,
            'training_outcomes_matched_to_outcomes': training_outcomes_matched,
            'training_outcomes_matched_to_outcomes_ids': training_outcomes_matched_to_outcomes_ids}


pickle_file_name = "ffc_data.p"


def save_data_as_pickle(data, path=pickle_file_name):
    pickle.dump(data, open(path, 'wb'))


def open_pickle_of_input_data(path=pickle_file_name):
    return pickle.load(open(path,'rb'))


def check_if_data_exists_if_not_open_and_read(path=pickle_file_name):
    if os.path.isfile(path):
        print "Pickle file already exists, just reading it in."
        print ""
        print ""
        return open_pickle_of_input_data(path)
    else:
        print "Pickle file does not exist, now reading in and processing data"
        print ""
        print ""
        data_loaded = data_open_and_process()
        save_data_as_pickle(data_loaded)
        return data_loaded


def remove_NA_from_outcomes_and_data(data, outcomes):
    try:
        len(outcomes[0])
        raise RuntimeError("This code only capable of taking 1-D list, not 2-D list")
    except TypeError:
        pass

    data_processed, outcomes_processed = zip(*((d, o) for d, o in zip(data, outcomes) if o != 'NA'))
    return (data_processed, outcomes_processed)


def precision_recall_etc(classification, actual_classification):
    """Given a pair of classifications and actual classifications,
    calculates various assessment parameters of the classification

    Parameters calculated: precision, recall, specificity, NPV, f1,
         tp (true positive), tn (true negative), fp (false positive),
         fn (false negative), accuracy

    Arguments:
        classification {[type]} -- the classifications you want to evaluate
        actual_classification {[list-like]} -- the reference, actual
                                  classifications to evaluate against

    Returns:
         dict -- a dictionary which can access all the values in the
                description above, with keys matching the values in the
                description above.


    Raises:
        RuntimeError -- len() of the two function arguments not the same
    """
    if len(classification) != len(actual_classification):  # if lengths don't match
        raise RuntimeError("Lengths of arguments to accuracy_percentage \
                not the same")
    tp = fp = tn = fn = 0  # t=true, f=false, p=postive, n=negative
    for i in range(len(classification)):
        if actual_classification[i] == 1:  # actual sentiment is positive
            if classification[i] == actual_classification[i]:  # if matches
                tp += 1
            else:  # if doesn't match
                fn += 1
        else:  # actual sentiment is negative
            if classification[i] == actual_classification[i]:  # if matches
                tn += 1
            else:  # if doesn't match
                fp += 1

    # calculate the various performance metrics
    precision = float(tp)/float(tp + fp)
    recall = float(tp)/float(tp + fn)
    specificity = float(tn)/float(fp + tn)
    NPV = float(tn)/float(tn + fn)
    f1 = 2.*float(precision*recall)/float(precision + recall)

    return {'precision': precision, 'recall': recall,
            'specificity': specificity, 'NPV': NPV,
            'f1': f1, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'accuracy': float(tp + tn)/float(tp + fp + tn + fn)}
