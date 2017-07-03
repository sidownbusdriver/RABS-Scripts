import os, datetime
import numpy as np
import matplotlib as mpl
from scipy import ndimage
import datetime as dt
from scipy import stats
import numpy.ma as ma
import matplotlib.pyplot as plt

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

def cutData(x, N,):
	cut = runningMeanFast(x, N)
	cut_data = cut[::10]
	return cut_data
    
f = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cut_data/wx_data_824_concrete.dat'
data = np.recfromtxt(f, unpack=True, skip_header=1, skip_footer=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

s_up = data['SUp_Avg']
temp = data['Temp_C_Avg']
s_down = data['SDn_Avg'] # upwelling
l_up = data['LUpCo_Avg'] # downwelling
l_down = data['LDnCo_Avg'] # upwelling
net = data['Rn_Avg']
albedo = data['Albedo_Avg']
ws = data['WS_ms_Avg']
time = data['TIMESTAMP']
#print len(temp)

# Change dates to datetime object
dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time]
seconds = [dt.datetime.strftime(t, '%S') for t in dates]
#print seconds

'''
# Use for cutting down to 1min
date = []
for i in range(len(seconds)):
	if seconds[i] == '00':
		date.append(dates[i])
#print len(date)
'''

date = time[0::10]  # smooth data to every 20 minutes
print len(date)

#run_temps = runningMeanFast(temp, 2.0)
#cut_temps = run_temps[::2]

cut_temps = cutData(temp, 10.0)
#print cut_temps
cut_sup = cutData(s_up, 10.0)
cut_sdown = cutData(s_down, 10.0)
cut_lup = cutData(l_up, 10.0)
cut_ldown = cutData(l_down, 10.0)
cut_net = cutData(net, 10.0)
cut_albedo = cutData(albedo, 10.0)
cut_ws = cutData(ws, 10.0)
print len(cut_temps)

valid_data = np.column_stack((date,cut_temps,cut_sup,cut_sdown,cut_lup,cut_ldown,cut_net,cut_albedo,cut_ws))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/cut_concrete_824.csv', valid_data, fmt='%s', delimiter=',')



