import general_functions as general_f


stuff = general_f.data_open_and_process()
print stuff['survey_data'][0][0]
print stuff['survey_data'][0][-1]
print stuff['training_outcomes'][0][0]
print stuff['training_outcomes'][0][-1]
