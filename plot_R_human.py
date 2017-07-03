import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math
import Rab_functions as R

# Read in data
f1 = '/Users/ahardin/Documents/Journal_Articles/Rabs/new_cnr/tennis_808_RABS_B.txt'
#f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_629_30_backyard.dat'
f3 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_tennis.csv'
f4 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/new_theory_Rabs/est_rabs_tennis.csv'
'''
f5 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs/cnr_rabs_backyard.csv'
f6 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_backyard.csv'
f7 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/theory_Rabs/est_rabs_backyard.csv'

f8 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs/cnr_rabs_cut_MCOM_831.csv'
f9 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_MCOM_831.csv'
f10 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/theory_Rabs/est_rabs_MCOM_831.csv'
'''
f11 = '/Users/ahardin/Documents/Journal_Articles/Rabs/new_cnr/sand_630_RABS_B.txt'
f12 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_sand.csv'
f13 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/theory_Rabs/est_rabs_sand.csv'

data1 = np.genfromtxt(f1)
#data2 = np.recfromtxt(f2, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data3 = np.recfromtxt(f3, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data4 = np.recfromtxt(f4, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
'''
data5 = np.recfromtxt(f5, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data6 = np.recfromtxt(f6, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data7 = np.recfromtxt(f7, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')

data8 = np.recfromtxt(f8, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data9 = np.recfromtxt(f9, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data10 = np.recfromtxt(f10, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
'''
data11 = np.genfromtxt(f11)
data12 = np.recfromtxt(f12, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data13 = np.recfromtxt(f13, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')

date = data3['Date']
crt_rabs = data3['crt_Rabs']
est_rabs = data4['theory_Rabs']
#ws = data2['WS_ms_Avg']
#ws = ws[:510]
cnr_rabs = data1
#print np.mean(est_rabs)
'''
date_b = data5['Date']
crt_rabs_b = data6['crt_Rabs']
est_rabs_b = data7['theory_Rabs']
cnr_rabs_b = data5['cnr_Rabs']

date_m = data8['Date']
crt_rabs_m = data9['crt_Rabs']
est_rabs_m = data10['theory_Rabs']
cnr_rabs_m = data8['cnr_Rabs']
'''
date_s = data12['Date']
crt_rabs_s = data12['crt_Rabs']
est_rabs_s = data13['theory_Rabs']
cnr_rabs_s = data11

# Convert dates
dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in date]
#dates_b = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in date_b]
#dates_m = [dt.datetime.strptime(t, '%Y-%m-%d %H:%M:%S') for t in date_m]
dates_s = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in date_s]

#### Plot 2 things ############
# Tennis
plt.figure()
plt.subplot(2,1,1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, crt_rabs, color='blue', label='R$_{crt}$')
plt.plot(dates, cnr_rabs, color='black', label='R$_{cnr}$')
plt.plot(dates, est_rabs, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
#plt.legend(loc='best')
plt.ylim(350, 760)
#plt.tight_layout()

# Sand
plt.subplot(2,1,2)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_s, crt_rabs_s, color='blue', label='R$_{crt}$')
plt.plot(dates_s, cnr_rabs_s, color='black', label='R$_{cnr}$')
plt.plot(dates_s, est_rabs_s, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
plt.legend(loc='lower right', prop={'size':11})
plt.ylabel('W/m$^2$', fontsize=9)
plt.xlabel('Time', fontsize=9)
plt.ylim(350, 760)
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Journal_Articles/Rabs/Final/figures/new_three_Rabs.pdf', dpi=300)

'''
#PLot one surface at a time
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, crt_rabs, color='blue', label='R$_{crt}$')
plt.plot(dates, cnr_rabs, color='black', label='R$_{cnr}$')
plt.plot(dates, est_rabs, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major')
#plt.legend(loc='best', prop={'size':25})
plt.ylim(350, 760)
plt.title('Tennis Court')
plt.ylabel('W/m$^2$')
plt.xlabel('Time')
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/Thesis/figures_for_powerpoint/tennis_Rabs.pdf', dpi=300)

# Plotting Rabs from CRT and Net Radiometer, and estimated Rabs
plt.figure()
plt.subplot(2,2,1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, crt_rabs, color='blue', label='R$_{crt}$')
plt.plot(dates, cnr_rabs, color='black', label='R$_{cnr}$')
plt.plot(dates, est_rabs, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
#plt.legend(loc='best')
plt.ylim(350, 760)
#plt.tight_layout()

plt.subplot(2,2,2)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_b, crt_rabs_b, color='blue', label='R$_{crt}$')
plt.plot(dates_b, cnr_rabs_b, color='black', label='R$_{cnr}$')
plt.plot(dates_b, est_rabs_b, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
#plt.legend(loc='best')
plt.ylim(350, 760)
#plt.tight_layout()

plt.subplot(2,2,3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_m, crt_rabs_m, color='blue', label='R$_{crt}$')
plt.plot(dates_m, cnr_rabs_m, color='black', label='R$_{cnr}$')
plt.plot(dates_m, est_rabs_m, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
#plt.legend(loc='best')
plt.ylim(350, 760)
#plt.tight_layout()

plt.subplot(2,2,4)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates_s, crt_rabs_s, color='blue', label='R$_{crt}$')
plt.plot(dates_s, cnr_rabs_s, color='black', label='R$_{cnr}$')
plt.plot(dates_s, est_rabs_s, color='green', label='R$_{est}$')
plt.tick_params(axis='both', which='major', labelsize=7)
plt.legend(loc='best', prop={'size':11})
plt.ylabel('W/m$^2$', fontsize=9)
plt.xlabel('Time', fontsize=9)
plt.ylim(350, 760)
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/Thesis/figures/three_Rabs.pdf', dpi=300)

# Plotting CNR rabs
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, cnr_rabs)
plt.title('R$_{abs}$ from CNR over Wet Grass')
plt.ylabel('W/m$^2$')
plt.xlabel('Time')
#plt.ylim(340,760)
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/cnr_Rabs/cnr_rabs_park_corr.png')

# Plot 2 things on one graph
fig, ax1 = plt.subplots()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#plt.hold(True)
lns1 = ax1.plot(dates, crt_rabs, color='red', label='R$_{crt}$')
ax1.set_xlabel('Time')
ax1.set_ylabel('W/m$^2$')

ax2 = ax1.twinx()
lns2 = ax2.plot(dates, ws, color='green', label='WS')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.set_ylabel('Wind Speed (m/s)')

# Legend
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='best')

#ax1.set_ylim(0, 450)
#ax2.set_ylim(29, 44)
ax1.set_title('Wind Speed and R$_{abs}$ over Dry Grass')
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/crtRabs_and_ws/crt_ws_backyard.png')
#plt.show() 
'''


