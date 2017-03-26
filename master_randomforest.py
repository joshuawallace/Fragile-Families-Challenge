#############
# Created 3-17-17 by JJW
# For the Fragile Families Challenge
# Implements scikit-learn's linear regression classifier
# on the FFC data
#
# AGBTG
# ###########
# This website helped me: http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html#sklearn.tree.DecisionTreeRegressor

import matplotlib
matplotlib.use('Agg')

#from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import Ridge
#from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
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
model_type = "randomforest"

# Various parameters that can be hard coded instead of read in as command line arguments
# imputation_strategy = "most_frequent"
# frac_missing_values_cutoff = 0.85
# K_max = 200
# K_min = 19
# K_space = 20
n_estimators = 15

if len(sys.argv) != 9:
    raise RuntimeError("Was expecting 8 arguments:\nimputation_strategy (string)\nfrac_missing_values_cutoff (between 0 and 1)\nK_min\nK_max\nK_space\nmax_depth_min\nmax_depth_max\nspace_max_depth")

imputation_strategy = sys.argv[1]  # which imputation strategy to use
frac_missing_values_cutoff = float(sys.argv[2])  # The fraction of unusable values a column has to have to be ignored
K_max = int(sys.argv[3])  # Maximum value for the k in the K-best feature selection 
K_min = int(sys.argv[4])  # Minimum value "                                       "
K_space = int(sys.argv[5])  # The spacing between k-values to try out, as defined by the range() function
if K_space > 0:
    K_space = -1 * K_space  # Make it negative so it counts down
max_depth_min = int(sys.argv[6])  # Minimum value of hyperparameter max_depth to try
max_depth_max = int(sys.argv[7])  # Maximum "                                      "
num_max_depth = int(sys.argv[8])   # Number of max depth to try, 

# If K values are mixed up
if K_max < K_min:
    print "Mixed up K_max and K_min values, correcting"
    temp = K_max
    K_max = K_min
    K_min = temp

# If max_depth values are mixed up
if max_depth_max < max_depth_min:
    print "Mixed up max_depth_max and max_depth_min values, correcting"
    temp = max_depth_max
    max_depth_max = max_depth_min
    max_depth_min = temp

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

# Set up empty lists to collect the mean squared error and
# R^2 error over the different values for K-best
mean_squared_error = []
r_squared_error = []

# The different values to use to K-best
k_values = range(K_max, K_min, K_space)
print k_values
print "Those are the k_values"

# Set up the different values of max_depth that will be used, spaced logairthmically
max_depths = np.linspace(max_depth_min, max_depth_max, num_max_depth)
for i in range(len(max_depths)):
    max_depths[i] = int(max_depths[i])

# Loop over the different values for K-best
for val in k_values:
    print "-------------------------------------"
    print "K-value being used: " + str(val)

    # Set up the feature selection instance
    feature_sel = SelectKBest(score_func=f_regression, k=val)

    # Set up some empty lists for collecting values
    mean_squared_error_this_k = []
    r_squared_error_this_k    = []

    # Loop over max_depths
    for max_depth in max_depths:
        print "   max_depth being used:  " + str(max_depth)

        # Set up the ML model
        regressor = RandomForestRegressor(n_jobs=2,n_estimators=n_estimators,criterion='mae',max_depth=max_depth)

        # Set up the pipeline
        pipeline = Pipeline([('select', feature_sel),
                        ('regression', regressor)])

        # Some empty lists to collect info for later use
        predicted_outcomes = []
        actual_outcomes    = []
        r_squared_error_this_max_depth = []

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
            r_squared_error_this_max_depth.append(r_squared_prediction)

        # Calculate, print, and save the mean squared error across all the folds
        mse = general_f.mean_squared_error(predicted_outcomes, actual_outcomes)
        print "Overall mean squared error: " + str(mse)
        mean_squared_error_this_k.append(mse)

        # Also, save the r_squared_errors across all the folds
        r_squared_error_this_k.append(r_squared_error_this_max_depth)

        # Plot some dianostic figures
        fig = lar.plot_predict_actual_pairs(predicted_outcomes, actual_outcomes)
        fig.savefig("pdf/" + model_type + "_max_depth" + str(max_depth) + "_nestimators" + str(n_estimators) + "_k" + str(val) + "_imp_" + imputation_strategy + "_cutoff" + str(frac_missing_values_cutoff) + ".png")
        plt.close(fig)

    # Save the error values for this particular iteration of k
    mean_squared_error.append(mean_squared_error_this_k)
    r_squared_error.append(r_squared_error_this_k)

# Plot some overall diagnostic plots
figs = lar.plot_errors_func_k_alpha(mean_squared_error, r_squared_error, k_values, max_depths)
figs[0].savefig("pdf/" + "overallerrplot_MSE_" + model_type + "_imp_" + imputation_strategy + "_nestimators" + str(n_estimators) + "_cutoff" + str(frac_missing_values_cutoff) + ".pdf")
figs[1].savefig("pdf/" + "overallerrplot_R2mean_" + model_type + "_imp_" + imputation_strategy + "_nestimators" + str(n_estimators) + "_cutoff" + str(frac_missing_values_cutoff) + ".pdf")
figs[2].savefig("pdf/" + "overallerrplot_R2media_" + model_type + "_imp_" + imputation_strategy + "_nestimators" + str(n_estimators) + "_cutoff" + str(frac_missing_values_cutoff) + ".pdf")
