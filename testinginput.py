import general_functions as general_f


outcomes = general_f.read_in_data('../data/train.csv')

survey_data = general_f.read_in_data('../data/background.csv')

outcomes_NAall_removed = general_f.remove_lines_with_all_NA(outcomes)


twople = general_f.match_up_data_with_training_set_of_outcomes(survey_data, outcomes_NAall_removed, clean_up_training=True)
