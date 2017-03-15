import general_functions as general_f


header, outcomes = general_f.read_in_data('../data/train.csv')

print "part 2"
print ""
print ""
header, survey_data = general_f.read_in_data('../data/background.csv')#_forpractice.csv')
#print survey_data[0]

outcomes_NAall_removed = general_f.remove_lines_with_all_NA(outcomes)
print outcomes_NAall_removed[0]


twople = general_f.match_up_data_with_training_set_of_outcomes(survey_data, outcomes_NAall_removed, clean_up_training=True)
