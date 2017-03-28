#############
# Created 3-17-17 by JJW
# For the Fragile Families Challenge
# Implements scikit-learn's linear regression classifier
# on the FFC data
#
# AGBTG
# ###########
# This website helped me: http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html#sklearn.tree.DecisionTreeRegressor

from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import Imputer
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import KFold

import general_functions as general_f
import data_postprocess as postprocess

# Various parameters that can be adjusted
# Hardcoded to the values found best for this model
imputation_strategy = "most_frequent"
frac_missing_values_cutoff = 0.6
K = 35
max_depth = 3

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
k_fold = KFold(n_splits=50, shuffle=True)

# Set up empty lists to collect info used later
r_squared_error = []
predicted_outcomes = []
actual_outcomes    = []

# Set up the feature selection instance
feature_sel = SelectKBest(score_func=f_regression, k=K)

# Set up the ML model
regressor = DecisionTreeRegressor(criterion='mae',max_depth=max_depth)

# Set up the pipeline
pipeline = Pipeline([('select', feature_sel),
                ('regression', regressor)])

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
    r_squared_error.append(r_squared_prediction)

# Calculate, print, and save the mean squared error across all the folds
mse = general_f.mean_squared_error(predicted_outcomes, actual_outcomes)

print "Mean, median, 95% confidence intervals for MSE:"
print np.mean(mse)
print np.median(mse)
print np.percentile(mse,(2.28,97.72),interpolation='linear')

print ""
print "Mean, median, 95% confidence intervals for R^2:"
print np.mean(r_squared_error)
print np.median(r_squared_error)
print np.percentile(r_squared_error,(2.28,97.72),interpolation='linear')
print ""
print ""
print ""
