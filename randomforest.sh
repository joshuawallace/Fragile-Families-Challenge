python master_randomforest.py "most_frequent" 1.1 19 500 -100 39 201 40 >& randomforest_mf_1.1.txt&
python master_randomforest.py "mean" 1.1 19 500 -100 39 201 40 >& randomforest_mn_1.1.txt&
python master_randomforest.py "median" 1.1 19 500 -100 39 201 40 >& randomforest_md_1.1.txt&

python master_randomforest.py "most_frequent" 0.7 19 500 -100 39 201 40 >& randomforest_mf_0.7.txt&

python master_randomforest.py "most_frequent" 0.5 19 500 -100 39 201 40 >& randomforest_mf_0.5.txt&
