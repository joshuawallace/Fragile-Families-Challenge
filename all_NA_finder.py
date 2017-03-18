import numpy as np

for j in range(len(data['survey_data_matched_to_outcomes'][0])):
    if all('NA' == item[j] for item in data['survey_data_matched_to_outcomes'] ):
        all_NAN_j.append(j)

np.savetxt("allNA.txt",all_NAN_j,fmt="%d")
print len(data['survey_data_matched_to_outcomes'][0])
