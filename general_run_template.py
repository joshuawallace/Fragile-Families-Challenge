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

import general_functions as general_f

data = general_f.check_if_data_exists_if_not_open_and_read()

if 'fathid1' in data['survey_data_header']:
    print "found fathid1"
    data['survey_data_header'].index('fathid1')

import csv
writer = csv.writer(open("looking_at.csv",'w'))
for row in data['survey_data_matched_to_outcomes']:
    writer.writerow(row)


data_to_use, outcomes_to_use = general_f.remove_NA_from_outcomes_and_data(data['survey_data_matched_to_outcomes'], [item[1] for item in data['training_outcomes_matched_to_outcomes']])

for i in range(len(data_to_use)):
    for j in range(len(data_to_use[i])):
        if data_to_use[i][j] == 'NA':
            data_to_use[i][j] = np.nan

imputation = Imputer(missing_values='NaN', strategy='most_frequent', verbose=10)
data_to_use = imputation.fit_transform(data_to_use)

data_in_reserve = data_to_use[-200:]
outcomes_in_reserve = outcomes_to_use[-200:]

data_to_use = data_to_use[:-200]
outcomes_to_use = outcomes_to_use[:-200]


regressor = LinearRegression(n_jobs=4,fit_intercept=True)

regressor.fit(data_to_use, outcomes_to_use)

prediction = regressor.predict(data_in_reserve)
mean_squared_error = general_f.mean_squared_error(prediction, outcomes_in_reserve)
print "Mean squared error: " + str(mean_squared_error)

r_squared_prediction = regressor.score(data_in_reserve, outcomes_in_reserve)
print "R^2 error: " + str(r_squared_prediction)

"""print outcomes_to_use[0:25]
print data_test[0:25]

for i in range(len(data_test)):
    if abs(data_test[i] - outcomes_to_use[i]) >= 1e-6:
        print str(data_test[i]) + "    " + str(outcomes_to_use[i])"""
