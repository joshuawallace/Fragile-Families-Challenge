python master_ridge.py "most_frequent" 1.1 9 250 -10 0.001 1.0 10 > ridge_mf_1.1.txt&
python master_ridge.py "mean" 1.1 9 250 -10 0.001 1.0 10 > ridge_mn_1.1.txt&
python master_ridge.py "median" 1.1 9 250 -10 0.001 1.0 10 > ridge_md_1.1.txt&

python master_ridge.py "most_frequent" 0.7 9 250 -10 0.001 1.0 10 > ridge_mf_0.7.txt&

python master_ridge.py "most_frequent" 0.5 9 250 -10 0.001 1.0 10 > ridge_mf_0.5.txt&
