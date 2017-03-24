#python master.py "most_frequent" 1.1 9 250 -10 > linear_mf_1.1.txt &
python master.py "mean" 1.1 9 250 -10 > linear_mn_1.1.txt&
python master.py "median" 1.1 9 250 -10 > linear_md_1.1.txt&
python master.py "most_frequent" 0.9 9 250 -10> linear_mf_0.9.txt &
python master.py "most_frequent" 0.8 9 250 -10 > linear_mf_0.8.txt&
python master.py "most_frequent" 0.7 9 250 -10> linear_mf_0.7.txt &

python master.py "most_frequent" 0.5 9 250 -10> linear_mf_0.5.txt &
