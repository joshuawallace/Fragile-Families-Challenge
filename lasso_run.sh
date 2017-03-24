python master_lasso.py "most_frequent" 1.1 9 250 -10 0.001 10. 10 > lasso_mf_1.1.txt&
python master_lasso.py "mean" 1.1 9 250 -10 0.001 10 10 > lasso_mn_1.1.txt&
python master_lasso.py "median" 1.1 9 250 -10 0.001 10 10 > lasso_md_1.1.txt&

python master_lasso.py "most_frequent" 0.7 9 250 -10 0.001 10 10 > lasso_mf_0.7.txt&

python master_lasso.py "most_frequent" 0.5 9 250 -10 0.001 10 10 > lasso_mf_0.5.txt&
