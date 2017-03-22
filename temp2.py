#############
# Created 3-17-17 by JJW
# For the Fragile Families Challenge
# Implements scikit-learn's linear regression classifier
# on the FFC data
#
# AGBTG
# ###########
# This website helped me: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html


#Let's also try ridge and lasso regression

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import Imputer
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

import general_functions as general_f
import data_postprocess as postprocess
import look_at_results as lar

data = general_f.check_if_data_exists_if_not_open_and_read()


data_to_use, outcomes_to_use = postprocess.remove_NA_from_outcomes_and_data(data['survey_data_matched_to_outcomes'], [item[1] for item in data['training_outcomes_matched_to_outcomes']])

data_to_use = postprocess.convert_NA_values_to_NaN(data_to_use, also_convert_negatives=False, deepcopy=False)

imputation = Imputer(missing_values='NaN', strategy='most_frequent', verbose=10)
data_to_use = imputation.fit_transform(data_to_use)

data_in_reserve = data_to_use[-200:]
outcomes_in_reserve = outcomes_to_use[-200:]

data_to_use = data_to_use[:-200]
outcomes_to_use = outcomes_to_use[:-200]


feature_sel = SelectKBest(score_func=f_regression, k=150)
regressor = LinearRegression(n_jobs=4,fit_intercept=True)

pipeline = Pipeline([('select', feature_sel),
                        ('regression', regressor)])

pipeline.fit(data_to_use, outcomes_to_use)

prediction = pipeline.predict(data_in_reserve)
mean_squared_error = general_f.mean_squared_error(prediction, outcomes_in_reserve)
print "Mean squared error: " + str(mean_squared_error)

r_squared_prediction = pipeline.score(data_in_reserve, outcomes_in_reserve)
print "R^2 error: " + str(r_squared_prediction)

fig = lar.plot_predict_actual_pairs(prediction, outcomes_in_reserve)
fig.savefig("temp2.pdf")
