import numpy as np
import os
import general_functions as general_f

try:
    os.remove(general_f.pickle_file_name)
except OSError:
    pass

data = general_f.check_if_data_exists_if_not_open_and_read(remove_bad_columns=False)

fathid_column = [i for i in range(len(data['survey_data_header'])) if 'fathid' in data['survey_data_header'][i]]
print "Father ID columns: " + str(fathid_column)

mothid_column = [i for i in range(len(data['survey_data_header'])) if 'mothid' in data['survey_data_header'][i]]
print "Mother ID columns: " + str(mothid_column)

all_NA_j = []

for j in range(len(data['survey_data_matched_to_outcomes'][0])):
    if all('NA' == item[j] for item in data['survey_data_matched_to_outcomes']):
        all_NA_j.append(j)
    elif all('Missing' == item[j] for item in data['survey_data_matched_to_outcomes']):
        all_NA_j.append(j)

print "Number of all NA or all missing columns: " + str(len(all_NA_j))

all_the_same_j = []

for j in range(len(data['survey_data_matched_to_outcomes'][0])):
    if all(item[0] == item[j] for item in data['survey_data_matched_to_outcomes']):
        all_the_same_j.append(j)

print "Number of columns with all the same values: " + str(len(all_the_same_j))

date_column = data['survey_data_header'].index('cf4fint')  # No matter how hard I try, I can't seem to reliably be able to convert the date into the correct int, so just skipping it
print "Date column to ignore: " + str(date_column)

otherinfo_column_info_to_skip = ['hv5_ppvtae', 'hv5_wj9ae',  'hv5_wj10ae', 'hv5_dsae',
                                 'hv5_dspr', 'hv5_ppvtpr', 'hv5_wj9pr', 'hv5_wj10pr'
                                 ] #Things that aren't missing data that don't convert to numbers well
otherinfo_toignore = []
for item in otherinfo_column_info_to_skip:
    otherinfo_toignore.append(data['survey_data_header'].index(item))

info_literally_missing = []
"""
for i in range(len(data['survey_data_matched_to_outcomes'][0])):
    if any(val[i] == '' for val in data['survey_data_matched_to_outcomes']):
        info_literally_missing.append(i)

print "Info literally missing columns: " + str(len(info_literally_missing))"""


columns_to_ignore = fathid_column + mothid_column + all_NA_j + all_the_same_j + [date_column] + otherinfo_toignore + info_literally_missing
columns_to_ignore.sort(reverse=True)
print columns_to_ignore[:10]
print columns_to_ignore[-10:]

np.savetxt("columns_to_remove.txt", columns_to_ignore, fmt="%d")

os.remove(general_f.pickle_file_name)

