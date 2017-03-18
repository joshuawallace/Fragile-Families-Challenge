import general_functions as general_f


output = general_f.data_open_and_process()


print output['survey_data_matched_to_outcomes_ids'][0:25]
print output['survey_data_matched_to_outcomes_ids'][-10:]
print output['training_outcomes_matched_to_outcomes_ids'][0:25]
print output['training_outcomes_matched_to_outcomes_ids'][-10:]

general_f.save_data_as_pickle(output)