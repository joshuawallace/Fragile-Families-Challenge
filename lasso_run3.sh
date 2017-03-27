python master_lasso.py "most_frequent" 0.8 10 50 -1 0.00001 0.0001 7 >& lasso3_mf_0.8.txt&
python master_lasso.py "most_frequent" 0.6 10 50 -1 0.00001 0.0001 7 >& lasso3_mf_0.6.txt&
python master_lasso.py "median" 0.8 9 250 -10 0.00001 0.001 10 >& lasso3_md_0.8.txt&
python master_lasso.py "median" 0.6 9 250 -10 0.00001 0.001 10 >& lasso3_md_0.6.txt&

