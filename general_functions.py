########################
# Created 3-8-17 by JJW
# Some general use functions for the Fragile Families Challenge
#
#
########################

import copy


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

    return (header, the_data)


def remove_lines_with_all_NA(outcomes_data):
    print outcomes_data[0][3]
    # print outcomes_data[0][3].type
    print outcomes_data[0][3] == 'NA'
    print 'NA' in outcomes_data[0][3]
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
        print outcome_indices['gpa']
        print outcome_indices['grit']
        print outcome_indices['materialhardship']
        print outcome_indices['eviction']
        print outcome_indices['layoff']
        print outcome_indices['jobtraining']
        print i
        print outcome_indices[i]
        if 'NA' in outcomes_data[outcome_indices['gpa']] and \
         'NA' in outcomes_data[outcome_indices['grit']] and \
         'NA' in outcomes_data[outcome_indices['materialhardship']] and \
         'NA' in outcomes_data[outcome_indices['eviction']] and \
         'NA' in outcomes_data[outcome_indices['layoff']] and \
         'NA' in outcomes_data[outcome_indices['jobtraining']]:
            print "found some!"
            all_NA.append(True)
        else:  # Else append False
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

    survey_data_to_return = [list(survey_data[i]) for i in range(len(survey_data)) if
                             survey_data[i][-1] in training_data_ids]

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
    #print survey_data_ids[0:10]
    survey_data_matched_to_outcomes_ids = [line.pop(-1) for line in survey_data_matched]
    #print survey_data_matched_to_outcomes_ids[0:10]
    training_outcomes_ids = [line.pop(0) for line in training_outcomes]
    print ""
    print training_outcomes_ids[0:10]
    print training_outcomes[0]
    print training_outcomes_matched[0]
    print outcomes_NAall_removed[0]
    training_outcomes_NAall_removed_ids = [line.pop(0) for line in outcomes_NAall_removed] #outcomes_NAall_removed and training_outcomes_matched tied together
    print training_outcomes_NAall_removed_ids[0:10]
    print training_outcomes[0]
    print training_outcomes_matched[0]
    print outcomes_NAall_removed[0]
    print ""
    training_outcomes_matched_to_outcomes_ids = [line.pop(0) for line in training_outcomes_matched]
    print training_outcomes_matched_to_outcomes_ids[0:10]
    print training_outcomes[0]
    print training_outcomes_matched[0]
    print outcomes_NAall_removed[0]

    print "Done with input and processing."
    return {'survey_data_header': survey_data_header,
            'survey_data': survey_data,
            'suvey_data_ids': survey_data_ids,
            'survey_data_matched_to_outcomes': survey_data_matched,
            'survey_data_matched_to_outcomes_ids': survey_data_matched_to_outcomes_ids,
            'training_outcomes_header': training_outcomes_header,
            'training_outcomes': training_outcomes,
            'training_outcomes_ids': training_outcomes_ids,
            'training_outcomes_NAall_removed': outcomes_NAall_removed,
            'training_outcomes_NAall_removed_ids': training_outcomes_NAall_removed_ids,
            'training_outcomes_matched_to_outcomes': training_outcomes_matched,
            'training_outcomes_matched_to_outcomes_ids': training_outcomes_matched_to_outcomes_ids}


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
