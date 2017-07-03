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
f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_turf_901.dat'
data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

K_0 = 1367.0   # solar constant
Kt_meas = data['SUp_Avg']
#Kt_meas = Kt_meas[108:620]   
time = data['TIMESTAMP']
#time = time[108:620]
tao = np.arange(.5, .91, .01)

# These will change based on the site and day
A = 994.0
d = 244.0
lat = 33.550915
corr = -42.0     # based on month

# Change dates to datetime object
dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time]
compare_dates = [dt.datetime.strftime(t, '%H') for t in dates]
minutes = [dt.datetime.strftime(t, '%M') for t in dates]
t = np.array(compare_dates, 'float')
m = np.array(minutes, 'float')
m = m/60.0
tm = t+m
tm = np.around(tm, decimals=2)

Kt_es=[]
for i in range(len(tao)):
	for j in range(len(tm)):
		Kt_es.append(R.est_Kt(A ,lat, d, tm[j], corr, tao[i]))
Kt_es = np.array(Kt_es)
a = np.split(Kt_es, 41)

rmse=[]
for i in range(len(tao)):
	rmse.append(np.sqrt(mean_squared_error(Kt_meas, a[i])))
#print rmse

# Finds transmissivity with least RMSE
rmse_min = np.min(rmse)
index = np.argmin(rmse)
tao_best = tao[index]
print tao_best

############### Using other method for Kt ##############################
Kt_kp = []
for i in range(len(tao)):
	for j in range(len(tm)):
		Kt_kp.append(R.est_Kp(A ,lat, d, tm[j], corr, tao[i]))
Kt_kp = np.array(Kt_kp)
b = np.split(Kt_kp, 41)

rmse_kp=[]
for i in range(len(tao)):
	rmse_kp.append(np.sqrt(mean_squared_error(Kt_meas, b[i])))
#print rmse

# Finds transmissivity with least RMSE
rmse_min_kp = np.min(rmse_kp)
index_kp = np.argmin(rmse_kp)
tao_best_kp = tao[index_kp]
print tao_best_kp

# Plotting
plt.figure()
plt.plot(tao, rmse)
plt.xlabel('Atmospheric Transmittance')
plt.ylabel('RMSE (W/m$^2$)')
plt.title('Turf RMSE (Kd+Kb)')
plt.text(.8, 200, 'min='+str(tao_best))
plt.xlim(.5, .9)
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/test/t_turf_kd_kb.pdf')

# Plotting
plt.figure()
plt.plot(tao, rmse_kp)
plt.xlabel('Atmospheric Transmittance')
plt.ylabel('RMSE (W/m$^2$)')
plt.title('Turf RMSE (Kp)')
plt.text(.8, 200, 'min='+str(tao_best_kp))
plt.xlim(.5, .9)
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/test/t_turf_kp.pdf')


