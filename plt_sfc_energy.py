import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/energy_budget/sand.csv'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_630_sand.dat'
f3 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/energy_budget/backyard.csv'
f4 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_629_backyard.dat'

data = np.recfromtxt(f1, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data2 = np.recfromtxt(f2, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data3 = np.recfromtxt(f3, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data4 = np.recfromtxt(f4, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

time_sand = data['Time']
qh_sand = data['Qh']
qe_sand = data['Qe']
qnet_sand = data2['Rn_Avg']

time_back = data3['Time']
qh_back = data3['Qh']
qe_back = data3['Qe']
qnet_back = data4['Rn_Avg']

dates_sand = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time_sand]
dates_back = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time_back]

# Plotting
plt.figure()
plt.subplot(2,1,1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_sand, qnet_sand, label='Q$^*$', color='black')
plt.plot(dates_sand, qh_sand, label='Q$_H$', color='red')
plt.plot(dates_sand, qe_sand, label='Q$_E$', color='green')
plt.ylim(-120,700)
plt.xlabel('Time')
plt.ylabel('W/m$^2$')
#plt.legend(loc='best')

plt.subplot(2,1,2)
plt.subplots_adjust(right=2.0)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_back, qnet_back, label='Q$^*$', color='black')
plt.plot(dates_back, qh_back, label='Q$_H$', color='red')
plt.plot(dates_back, qe_back, label='Q$_E$', color='green')
plt.ylim(-120,700)
plt.xlabel('Time')
plt.ylabel('W/m$^2$')
plt.legend(loc='best', prop={'size':9})
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/Thesis/figures/sfc_energy.pdf', dpi=300)








