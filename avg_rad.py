import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats

f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_808_tennis.dat'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_tennis.csv'
data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype='float', names=True, delimiter=',', missing_values='"NAN"')
data2 = np.recfromtxt(f2, unpack=True, dtype=None, names=True, delimiter=',')

# Data
date = data['TIMESTAMP']
record = data['RECORD']
s_up = data['SUp_Avg']   # downwelling
s_down = data['SDn_Avg'] # upwelling
l_up = data['LUpCo_Avg'] # downwelling
l_down = data['LDnCo_Avg'] # upwelling
net = data['Rn_Avg']
albedo = data['Albedo_Avg']

temp = data['AirTC_Avg']
ws = data['WS_ms_Avg']
crt_rabs = data2['crt_Rabs']
#temp = temp[:510]
#ws = ws[:510]
#crt_rabs = crt_rabs[:510]

temp_avg = stats.nanmean(temp)
ws_avg = stats.nanmean(ws)
crt_rabs_avg = stats.nanmean(crt_rabs)

print('Temp avg:'), temp_avg
print('WS avg:'), ws_avg
print('R_crt avg:'), crt_rabs_avg


'''
# Calculate averages
s_up_avg = stats.nanmean(s_up)
s_down_avg = stats.nanmean(s_down)
l_up_avg = stats.nanmean(l_up)
l_down_avg = stats.nanmean(l_down)
net_avg = stats.nanmean(net)
albedo_avg = stats.nanmean(albedo)

# Print out averages
print('Downwelling SW Average:'), s_up_avg
print('Upwelling SW Average:'), s_down_avg
print('Downwelling LW Avg:'), l_up_avg
print('Upwelling LW Avg:'), l_down_avg
print('Net Radiation Avg:'), net_avg
print('Average Albedo:'), albedo_avg
'''




