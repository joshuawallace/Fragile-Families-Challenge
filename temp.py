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

import general_functions as general_f

data = general_f.check_if_data_exists_if_not_open_and_read()

all_NAN_j = []

import csv
writer = csv.writer(open("looking_at.csv",'w'))
for row in data['survey_data_matched_to_outcomes']:
    writer.writerow(row)


data_to_use, outcomes_to_use = general_f.remove_NA_from_outcomes_and_data(data['survey_data_matched_to_outcomes'], [item[1] for item in data['training_outcomes_matched_to_outcomes']])

for i in range(len(data_to_use)):
    for j in range(len(data_to_use[i])):
        if data_to_use[i][j] == "11511":
                print "11511"
                print i
                print j
num = 0
imputation = Imputer(missing_values='NA', strategy='most_frequent',verbose=1)
h = imputation.fit_transform(data_to_use)
for line in data_to_use:
    if 'NA' in line:
        num += 1
        print "whoops2"
print num
num2 = 0
for line in h:
    if 'NA' in line:
        num2+=1
print num2
print len(data_to_use)

pipeline = Pipeline([("imputer", Imputer(missing_values='NA', strategy='most_frequent')),
                    ("regression", LinearRegression(n_jobs=4))])

data_to_use_transformed = pipeline.fit_transform(data_to_use, outcomes_to_use)

data_test = pipeline.predict(data_to_use)
