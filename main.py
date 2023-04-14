#Main python pipeline
from utils.util import *

#with calibration data
names = ['Q1', 'Q2', 'Q3', 'Q4', 'CC']
for name in names:
    load_data(name)
d_cal = calibration_data(names)   
path = plot_calibration_data(d_cal, "test123") 
print("plot saved to: " + path)
d_stats = compute_stats(d_cal)
for name in names:
    print(name)
    print(d_stats[name].loc['avg'])
    print(d_stats[name].loc['stdev'])

#test
conf_x, error = find_zscore(d_stats, [0.1, 0.1, 0.1])
print(conf_x)
print(min(error, key=error.get))


#Test 001


