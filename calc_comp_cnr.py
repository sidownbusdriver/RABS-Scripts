import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math
import Rab_functions as R
from sklearn.metrics import mean_squared_error

f1 = '/Users/ahardin/Documents/Journal_Articles/Rabs/comp_cnr/tennis_808_RABS_all.txt'
f2 = '/Users/ahardin/Documents/Journal_Articles/Rabs/Rabs_all_comp/tennis_808_RABS.txt'
data = np.genfromtxt(f1)
data2 = np.genfromtxt(f2)

# Get the data from the file
Kin = data2[:,0]
Kup = data2[:,1]
Lin = data2[:,2]
Lup = data2[:,3]
total = data[:,4]

# Calculate average of each
Kin_av = stats.nanmean(Kin)
Kup_av = stats.nanmean(Kup)
Lin_av = stats.nanmean(Lin)
Lup_av = stats.nanmean(Lup)
total_av = stats.nanmean(total)

# Calculate percentage of each component
Kinp = (Kin_av/total_av)*100.0
Kupp = (Kup_av/total_av)*100.0
Linp = (Lin_av/total_av)*100.0
Lupp = (Lup_av/total_av)*100.0

# Print out percentages and averages
print('Averages')
print('Kin:'), Kin_av
print('Kup:'), Kup_av
print('Lin:'), Lin_av
print('Lup:'), Lup_av
print('Rcnr:'), total_av

print('Percentages')
print('Kin:'), Kinp
print('Kup:'), Kupp
print('Lin:'), Linp
print('Lup:'), Lupp




