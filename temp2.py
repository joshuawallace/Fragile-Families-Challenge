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
import look_at_results as lar

data = general_f.check_if_data_exists_if_not_open_and_read()


data_to_use, outcomes_to_use = postprocess.remove_NA_from_outcomes_and_data(data['survey_data_matched_to_outcomes'], [item[2] for item in data['training_outcomes_matched_to_outcomes']])

data_to_use = postprocess.convert_NA_values_to_NaN(data_to_use, also_convert_negatives=False, deepcopy=False)

data_to_use = postprocess.remove_columns_with_large_number_of_missing_values(data_to_use, 0.85, deepcopy=False)

imputation = Imputer(missing_values='NaN', strategy='mean')  # mean, median, most_frequent
data_to_use = imputation.fit_transform(data_to_use)

data_to_use = np.asarray(data_to_use)
outcomes_to_use = np.asarray(outcomes_to_use)

k_fold = KFold(n_splits=20, shuffle=True)

regressor = LinearRegression(n_jobs=4, fit_intercept=True)

mean_squared_error = []
r_squared_error = []
k_values = range(1000, 50, -50)

for val in k_values:
    print "-------------------------------------"
    print "K-value being used: " + str(val)
    feature_sel = SelectKBest(score_func=f_regression, k=100)

    pipeline = Pipeline([('select', feature_sel),
                        ('regression', regressor)])

    predicted_outcomes = []
    actual_outcomes    = []
    r_squared_error_justthisKvalue = []

    for training_indices, testing_indices in k_fold.split(data_to_use):

        pipeline.fit(data_to_use[training_indices], outcomes_to_use[training_indices])
        prediction = pipeline.predict(data_to_use[testing_indices])
        predicted_outcomes.extend(prediction)
        actual_outcomes.extend(outcomes_to_use[testing_indices])

        r_squared_prediction = pipeline.score(data_to_use[testing_indices], outcomes_to_use[testing_indices])
        print "R^2 error: " + str(r_squared_prediction)
        r_squared_error_justthisKvalue.append(r_squared_prediction)

    mse = general_f.mean_squared_error(predicted_outcomes, actual_outcomes)
    print "Overall mean squared error: " + str(mse)
    mean_squared_error.append(mse)
    r_squared_error.append(r_squared_error_justthisKvalue)

# print mean_squared_error
# print r_squared_error

#fig = lar.plot_predict_actual_pairs(prediction, outcomes_in_reserve)
#fig.savefig("temp2.pdf")
