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
import sys
import matplotlib.pyplot as plt

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import KFold

import general_functions as general_f
import data_postprocess as postprocess
import look_at_results as lar

# Name of the model type, for saving the figures
model_type = "linear"

# Various parameters that can be hard coded instead of read in as command line arguments
# imputation_strategy = "most_frequent"
# frac_missing_values_cutoff = 0.85
# K_max = 200
# K_min = 19
# K_space = 20

# Check that there's enough command line arguments
if len(sys.argv) != 6:
    raise RuntimeError("Was expecting 5 arguments:\nimputation_strategy (string)\nfrac_missing_values_cutoff (between 0 and 1)\nK_min\nK_max\nK_space")

imputation_strategy = sys.argv[1]  # which imputation strategy to use
frac_missing_values_cutoff = float(sys.argv[2])  # The fraction of unusable values a column has to have to be ignored
K_max = int(sys.argv[3])  # Maximum value for the k in the K-best feature selection 
K_min = int(sys.argv[4])  # Minimum value "                                       "
K_space = int(sys.argv[5])  # The spacing between k-values to try out, as defined by the range() function
if K_space > 0:
    K_space = -1 * K_space  # Make it negative so it counts down

# If K values are mixed up
if K_max < K_min:
    print "Mixed up K_max and K_min values, correcting"
    temp = K_max
    K_max = K_min
    K_min = temp

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
data_to_use = postprocess.remove_columns_with_large_number_of_missing_values(data_to_use, frac_missing_values_cutoff, deepcopy=False)

# Impute the NaN values
imputation = Imputer(missing_values='NaN', strategy=imputation_strategy)  # mean, median, most_frequent
data_to_use = imputation.fit_transform(data_to_use)

# Convert to Numpy arrays so that the indices can be accessed with a list later
data_to_use = np.asarray(data_to_use)
outcomes_to_use = np.asarray(outcomes_to_use)

# Create a KFold instance
k_fold = KFold(n_splits=13, shuffle=True)

# Set up the ML model
regressor = LinearRegression(n_jobs=1, fit_intercept=True, copy_X=True)

# Set up empty lists to collect the mean squared error and
# R^2 error over the different values for K-best
mean_squared_error = []
r_squared_error = []

# The different values to use to K-best
k_values = range(K_max, K_min, K_space)

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

    # Plot some dianostic figures
    fig = lar.plot_predict_actual_pairs(predicted_outcomes, actual_outcomes)
    fig.savefig("pdf/" + model_type + "_k" + str(val) + "_imp_" + imputation_strategy + "_cutoff" + str(frac_missing_values_cutoff) + ".png")
    plt.close(fig)

# Plot some overall diagnostic figures
fig = lar.plot_errors_func_k_noalpha(mean_squared_error, r_squared_error, k_values)
fig.savefig("pdf/" + "overallerrplot_" + model_type + "_imp_" + imputation_strategy + "_cutoff" + str(frac_missing_values_cutoff) + ".pdf")
