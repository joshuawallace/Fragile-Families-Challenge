import numpy as np
import general_functions as general_f

data = general_f.check_if_data_exists_if_not_open_and_read(remove_bad_columns=False)

fathid_column = [i for i in range(len(data['survey_data_header'])) if 'fathid' in data['survey_data_header'][i]]
print "Father ID columns: " + str(fathid_column)

mothid_column = [i for i in range(len(data['survey_data_header'])) if 'mothid' in data['survey_data_header'][i]]
print "Mother ID columns: " + str(mothid_column)

all_NA_j = []

for j in range(len(data['survey_data_matched_to_outcomes'][0])):
    if all('NA' == item[j] for item in data['survey_data_matched_to_outcomes']):
        all_NA_j.append(j)

print "Number of all NA columns: " + str(len(all_NA_j))

all_the_same_j = []

for j in range(len(data['survey_data_matched_to_outcomes'][0])):
    if all(item[0] == item[j] for item in data['survey_data_matched_to_outcomes']):
        all_the_same_j.append(j)

print "Number of columns with all the same values: " + str(len(all_the_same_j))

date_column = data['survey_data_header'].index('"cf4fint"')  # No matter how hard I try, I can't seem to reliably be able to convert the date into the correct int, so just skipping it
print "Date column to ignore: " + str(date_column)

columns_to_ignore = fathid_column + mothid_column + all_NA_j + all_the_same_j + [date_column]
columns_to_ignore.sort(reverse=True)
print columns_to_ignore[:10]
print columns_to_ignore[-10:]

np.savetxt("columns_to_remove.txt", columns_to_ignore, fmt="%d")
print len(data['survey_data_matched_to_outcomes'][0])
