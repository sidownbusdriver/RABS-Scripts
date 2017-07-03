import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

# Read in the data
#f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_806_asphalt.dat'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cut_concrete_824.csv'
#f3 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/rooftop_08312014.csv'
#data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data1 = np.recfromtxt(f2, unpack=True, dtype=None, names=True, delimiter=',')
#data2 = np.recfromtxt(f3, unpack=True, dtype=None, names=True, delimiter=',')

sigma = 5.67*10**-8;   # stephan-boltzman constant
rhoCp = 1212.0;        # volumetric heat capacity of air @ 20C
epsilon = 0.95;        # emissivity of cylinder

w_s = data1['WS_ms_Avg']
#w_s = w_s[:510]
T_air = data1['Temp']
#T_air = T_air[:510]
T_crt = data1['Temp_C_Avg']
#T_crt = T_crt[:510]
time = data1['TIMESTAMP']
#time = time[:510]
#print np.mean(T_crt)
#print np.mean(w_s)

def r_m(ws, d):
	"""Calculates the resistance of a cylinder to sensible heat transfer (s/m). Uses wind
	speed (m/s) and diameter of the cylinder (m)."""
	k = 22.2*10**-6   # thermal diffusivity of air (m^2/s)
	v = 1.55*10**-5   # kinematic viscosity of air (m^2/s)
	Pr = .71          # Prandtl number
	Re = (ws*d)/v
	if Re < 4000.0:
		A = .683
		n = .466
	elif Re >= 4000.0 and Re < 40000.0:
		A = .193
		n = .618
	elif Re > 40000.0:
		A = .0266
		n = .805
	rm = d/(A*(Re**n)*(Pr**.33)*k)
	return rm

rm = []
#Re = []
for i in range(len(w_s)):
	rm.append(r_m(w_s[i], .0095))
#rm = np.array(rm)
#print rm


T_crtK = 273.15 + T_crt
crt_rabs = .78*((epsilon*sigma*(T_crtK**4)) + (rhoCp*((T_crt-T_air)/rm)))
print stats.nanmean(crt_rabs)
print stats.nanmean(w_s)
print ('Air temp:'), stats.nanmean(T_air)
print ('CRT Temp:'), stats.nanmean(T_crt)

valid_data = np.column_stack((time, crt_rabs))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_concrete_824.csv', valid_data, fmt='%s', delimiter=',')







