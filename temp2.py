#############
# Created 3-17-17 by JJW
# For the Fragile Families Challenge
# Implements scikit-learn's linear regression classifier
# on the FFC data
#
# AGBTG
# ###########
# This website helped me: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.preprocessing import Imputer
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import KFold

import general_functions as general_f
import data_postprocess as postprocess

# Read in the data
data = general_f.check_if_data_exists_if_not_open_and_read()

# Clean up the outcomes and corresponding data if the outcome is NA
data_to_use, outcomes_to_use = postprocess.remove_NA_from_outcomes_and_data(
    data['survey_data_matched_to_outcomes'], [item[2] for  # item[2] corresponds to grit
    item in data['training_outcomes_matched_to_outcomes']])

# Converts all the NA values to NaN, so the imputer can impute over them
# Also convert negative values to NaN, if also_convert_negatives=True
data_to_use = postprocess.convert_NA_values_to_NaN(data_to_use,
                                also_convert_negatives=True, deepcopy=False)

# Remove columns that have a large fraction of values missing
data_to_use = postprocess.remove_columns_with_large_number_of_missing_values(data_to_use, 0.85, deepcopy=False)

# Impute the NaN values
imputation = Imputer(missing_values='NaN', strategy='most_frequent')  # mean, median, most_frequent
data_to_use = imputation.fit_transform(data_to_use)

# Convert to Numpy arrays so that the indices can be accessed with a list later
data_to_use = np.asarray(data_to_use)
outcomes_to_use = np.asarray(outcomes_to_use)

# Create a KFold instance
k_fold = KFold(n_splits=20, shuffle=True)

# Set up the ML model
regressor = LinearRegression(n_jobs=4, fit_intercept=True)

# Set up empty lists to collect the mean squared error and
# R^2 error over the different values for K-best
mean_squared_error = []
r_squared_error = []

# The different values to use to K-best
k_values = range(200, 19, -20)

# Loop over the different values for K-best
for val in k_values:
    print "-------------------------------------"
    print "K-value being used: " + str(val)

    # Set up the feature selection instance
    feature_sel = SelectKBest(score_func=f_regression, k=val)

    # Set up the pipeline
    pipeline = Pipeline([('select', feature_sel),
                        ('regression', regressor)])

    # Some empty lists to collect info for later use
    predicted_outcomes = []
    actual_outcomes    = []
    r_squared_error_justthisKvalue = []

    # Loop over the various folds
    for training_indices, testing_indices in k_fold.split(data_to_use):

        # Fit and predict
        pipeline.fit(data_to_use[training_indices], outcomes_to_use[training_indices])
        prediction = pipeline.predict(data_to_use[testing_indices])

        # Save the predicted and actual values
        predicted_outcomes.extend(prediction)
        actual_outcomes.extend(outcomes_to_use[testing_indices])

        # Calculate an R^2 value for the fold
        r_squared_prediction = pipeline.score(data_to_use[testing_indices], outcomes_to_use[testing_indices])
        print "R^2 error: " + str(r_squared_prediction)
        r_squared_error_justthisKvalue.append(r_squared_prediction)

    # Calculate, print, and save the mean squared error across all the folds
    mse = general_f.mean_squared_error(predicted_outcomes, actual_outcomes)
    print "Overall mean squared error: " + str(mse)
    mean_squared_error.append(mse)

    #Also, save the r_squared_errors across all the folds
    r_squared_error.append(r_squared_error_justthisKvalue)

# print mean_squared_error
# print r_squared_error

#fig = lar.plot_predict_actual_pairs(prediction, outcomes_in_reserve)
#fig.savefig("temp2.pdf")
