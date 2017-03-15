########################
# Created 3-8-17 by JJW
# Some general use functions for the Fragile Families Challenge
#
#
########################

import numpy as np


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
    the_data =[]
    with open(path, 'r') as f:
        the_data_readin = f.readlines()

    #the_data_readin = the_data_readin[:3]
    #for i in range(len(the_data_readin)):
    #        the_data_readin[i] = the_data_readin[i][0:5]
     
    #print the_data_readin
    #print the_data_readin[0]
    
    second_column_is_mothid1 = False
    if 'background.csv' in path:
        second_column_is_mothid1 = True

    for line in the_data_readin:
        #temp = line.split(',')
        if second_column_is_mothid1:
            the_data.append(line.split(',')[2:])
        else:
            the_data.append(line.split(','))
    #print the_data[-1]

    # Remove the header line, save it as its own thing
    header = the_data.pop(0)
    #the_data = the_data[1:]

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

    return (header, the_data)


"""def read_in_classifications(path):

    the_classification_data = np.genfromtxt(path, delimiter=',')

    return {'ID': the_classification_data[0],
            'gpa':  the_classification_data[1],
            'grit': the_classification_data}"""


def remove_lines_with_all_NA(outcomes_data):

    all_NA = []  # A list that will be filled with Boolean values,
                 # specifying whether all the outcomes are NA or not.
    for i in range(len(outcomes_data)):  # Loop through the data
        # If all six outcomes are 'NA',  append True to all_NA
        if outcomes_data[outcome_indices['gpa']] == 'NA' and \
         outcomes_data[outcome_indices['grit']] == 'NA' and \
         outcomes_data[outcome_indices['materialhardship']] == 'NA' and \
         outcomes_data[outcome_indices['eviction']] == 'NA' and \
         outcomes_data[outcome_indices['layoff']] == 'NA' and \
         outcomes_data[outcome_indices['jobtraining']] == 'NA':
            all_NA.append(True)
        else:  # Else append False
            all_NA.append(False)

    # Checking that all_NA is the appropriate length
    if len(outcomes_data) != len(all_NA):
        raise RuntimeError("For some reason, all_NA is not the proper length \
                (the same length as the input)")

    outcomes_data_removed = [outcomes_data[i] for i in range(len(outcomes_data)) if all_NA[i] == False]

    print str(len(outcomes_data_removed)) + " rows kept from the outcome data \
          out of " + str(len(outcomes_data))

    return outcomes_data_removed


def match_up_data_with_training_set_of_outcomes(survey_data, training_outcomes_data, clean_up_training=False):

    training_data_ids = []
    for i in range(len(training_outcomes_data)):
        training_data_ids.append(training_outcomes_data[i][outcome_indices['ID']])

    #print survey_data[0][-1]
    #print survey_data[1][-1]
    #print survey_data[2][-1]
    #print training_data_ids[-1]

    #print [survey_data[i][-1] for i in range(len(survey_data))]




    survey_data_to_return = [survey_data[i] for i in range(len(survey_data)) if
                             survey_data[i][-1] in training_data_ids]

    missing_matches = []


    survey_data_to_return_ids = [item[-1] for item in survey_data_to_return]

    for i in range(len(training_data_ids)):
        if training_data_ids[i] not in survey_data_to_return_ids:
            missing_matches.append(training_data_ids[i])

    if missing_matches:
        #print missing_matches
        print "************************"
        print "There were some id's in the training set of outcomes not in \
               the survey question data.  Specifically, " + \
               str(len(missing_matches)) + " id's."

    if clean_up_training == False or not missing_matches:
        if missing_matches:
            print "Doing nothing about the missing data..."
        training_data_to_return = training_outcomes_data

    else:
        "Matching the training outcomes to the survey data"
        training_data_to_return = training_outcomes_data
        missing_matches.sort(reverse="true")
        for i in missing_matches:
            training_data_to_return.pop(i)

    return (survey_data_to_return, training_data_to_return)


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
