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
from sklearn.preprocessing import Imputer
from sklearn.pipeline import Pipeline
import numpy as np
import csv

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import KFold

import general_functions as general_f
import data_postprocess as postprocess

# Various parameters that can be adjusted
# Hardcoded to the values found best for this model
imputation_strategy = "most_frequent"
frac_missing_values_cutoff = 0.6
K = 27


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
all_data_to_use = postprocess.convert_NA_values_to_NaN(data['survey_data'])

# Remove columns that have a large fraction of values missing
data_to_use, all_data_to_use = postprocess.remove_columns_with_large_number_of_missing_values(data_to_use, frac_missing_values_cutoff, deepcopy=False, extra_tagalong=all_data_to_use)

# Impute the NaN values
imputation = Imputer(missing_values='NaN', strategy=imputation_strategy)  # mean, median, most_frequent
#data_to_use = imputation.fit_transform(data_to_use)
#all_data_to_use = imputation.fit_transform(all_data_to_use)

# Convert to Numpy arrays so that the indices can be accessed with a list later
data_to_use = np.asarray(data_to_use)
all_data_to_use = np.asarray(all_data_to_use)
outcomes_to_use = np.asarray(outcomes_to_use)

# Set up the ML model
regressor = LinearRegression(n_jobs=4, fit_intercept=True, copy_X=True)

# Set up the feature selection instance
feature_sel = SelectKBest(score_func=f_regression, k=K)

# Set up the pipeline
pipeline = Pipeline([('imputer', imputation),
                     ('select', feature_sel),
                    ('regression', regressor)])

# Fit and predict
pipeline.fit(data_to_use, outcomes_to_use)
print "pipeline fitted, now predicting"
prediction = pipeline.predict(all_data_to_use)

# Now take super out-of-bounds values and put them in the appropriate range
num_toohigh = 0
num_toolow  = 0
for i in range(len(prediction)):
    if prediction[i] > 4.0:
        prediction[i] = 4.0
        num_toohigh += 1
    elif prediction[i] < 1.0:
        prediction[i] = 1.0
        num_toolow += 1

print "Number too high: " + str(num_toohigh)
print "Number too low:  " + str(num_toolow)

# Data to print out
list_to_return = []
list_to_return.append(["challengeID","gpa","grit","materialHardship","eviction","layoff","jobTraining"])
for i in range(len(prediction)):
    list_to_return.append([data['survey_data_ids'][i], 3.0, prediction[i], 0.2, 2, 2, 2])


with open("prediction.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(list_to_return)
