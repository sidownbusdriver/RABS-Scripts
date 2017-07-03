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

# Read in the data
#f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_MCOM_826.dat'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cut_green_904.csv'
#data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data = np.recfromtxt(f2, unpack=True, dtype=None, names=True, delimiter=',')

time = data['TIMESTAMP']
Kin = data['SUp_Avg']   # downwelling
Kup = data['SDn_Avg'] # upwelling
l_in = data['LUpCo_Avg'] # downwelling
l_down = data['LDnCo_Avg'] # upwelling
albedo = data['Albedo_Avg']
#time = time[:510]
#Kin = Kin[:510]
#Kup = Kup[:510]
#l_in = l_in[:510]
#l_down = l_down[:510]

# Make correction for longwave
A = 990.0
d = 247.0
lat = 33.516752
corr = -42.0     # based on month
tao = .65
r = .005   # radius of cylinder
skin_alb = .39
h = .1     # height of cylinder
A_eff = .78   # effective radiation area factor
A_cyl = R.Acyl(r, h)

# Change dates to datetime object
#dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time]
dates = [dt.datetime.strptime(t, '%m/%d/%y %H:%M') for t in time]
compare_dates = [dt.datetime.strftime(t, '%H') for t in dates]
minutes = [dt.datetime.strftime(t, '%M') for t in dates]
t = np.array(compare_dates, 'float')
t = t-1.0
m = np.array(minutes, 'float')
m = m/60.0
tm = t+m
tm = np.around(tm, decimals=2)

# Calculate Kb and Kd
Kb = R.Kb_cnr(Kin, A, lat, d, tm, corr, tao)
Kd = Kin - Kb
Kup = Kup + Kd
#Kb_abs = R.abs_Kb(Kb, lat, d, tm, corr, r, skin_alb)

# Calculate four components of Rabs
Kup_abs = R.abs_Kup(Kup, r, h, skin_alb)
Kin_abs = R.abs_Kin(Kin, r, h, skin_alb)
Lup_abs = R.abs_Lg(l_down, r, h)
Lin_abs = R.abs_La(l_in, r, h)

R_cnr = A_eff*((Kb_abs+Kin_abs+Lup_abs+Lin_abs)/A_cyl)
R_cnr_mean = stats.nanmean(R_cnr)
R_cnr_max = np.nanmax(R_cnr)
print ('Rcnr mean:'), R_cnr_mean
print ('R_cnr max:'), R_cnr_max
'''
# Plotting
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, R_cnr)
plt.xlabel('Time')
plt.ylabel('R$_{cnr}$ (W/m$^2$)')
plt.title('Radiation Absorbed by a Human Over MCOM Roof 8/31')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/cnr_Rabs/cnr_rabs_cut_MCOM_831.png')
#plt.show()

# Save file
valid_data = np.column_stack((time, R_cnr))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs/cnr_rabs_cut_green_904.csv', valid_data, fmt='%s', delimiter=',')
'''




