import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

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

# Read in the data
f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_630_sand.dat'
#f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/rooftop_08262014.csv'
data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
#data1 = np.recfromtxt(f2, unpack=True, dtype=None, names=True, delimiter=',')

sigma = 5.67*10**-8;   # stephan-boltzman constant
rhoCp = 1212.0;        # volumetric heat capacity of air @ 20C
epsilon = 0.95;        # emissivity of cylinder

w_s = data['WS_ms_Avg']
#w_s = w_s[:510]
T_air = data['AirTC_Avg']
T_airK = T_air + 273.15
#T_air = T_air[:510]
T_crt = data['Temp_C_Avg']
T_crtK = T_crt + 273.15
#T_crt = T_crt[:510]
time = data['TIMESTAMP']
#time = time[:510]

# Calculate means
T_crtK_avg = np.mean(T_crtK)
dT = T_crt-T_air

# Using actual data
rm = []
for i in range(len(w_s)):
	rm.append(r_m(w_s[i], .0095))
rm_mean = np.mean(rm)

# calculate Rabs
crt_rabs = .78*((epsilon*sigma*(T_crtK_avg**4)) + (rhoCp*((dT)/rm_mean)))

# Plotting
plt.figure()
plt.scatter(dT, crt_rabs)
#plt.plot(ws_cus, rm_ws_cus)
plt.grid()
#plt.title('Sensitivity of R$_{crt}$ to T$_{a}$ ')
#plt.xlabel('$T$$_{crt}$ ($\degree$$C$)')
plt.xlabel('$T_{crt}-T_a$ ($\degree$$C$)')
#plt.xlabel('Wind Speed ($ms^{-1}$)')
#plt.xlabel('$r_m$ ($sm^{-1}$)')
plt.ylabel('$R$$_{crt}$ ($W/m$$^2$)')
#plt.ylabel('$r_m$ ($sm^{-1}$)')
#plt.xlim(0, 10)
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/Thesis/figures/dT_Rcrt_sand.pdf', dpi=300)




'''
# Custom ranges
Ta_cus = np.arange(300.0, 320.1, .1)
Ta_mean = 308.9
Tcrt_cus = np.arange(300.0, 320.1, .1)
Tcrt_mean = 311.01
dT_cus = np.arange(-1.0, 10.1, .1)
dT_mean = 2.2
rm_cus = np.arange(10.0, 146.0, 1.0)
rm_mean = 40.0
ws_cus = np.arange(0.0, 10.05, .05)
ws_mean = 1.9
rm_ws_cus = []
for i in range(len(ws_cus)):
	rm_ws_cus.append(r_m(ws_cus[i], .0095))
rm_ws_cus = np.array(rm_ws_cus)
#print np.min(rm_ws_cus)

#rmtest = r_m(.05, .0095)
#print rmtest

# Averages
dT = T_crt-T_air
#dT_mean = stats.nanmean(dT)
T_crtK = 273.15 + T_crt
#T_crtK = np.mean(T_crtK)
#ws_avg = stats.nanmean(w_s)
#print ws_avg

# Calculate rm
rm = []
for i in range(len(w_s)):
	rm.append(r_m(w_s[i], .0095))
#rm = np.array(rm)
#rm_mean = stats.nanmean(rm)

#crt_rabs = .78*((epsilon*sigma*(T_crtK**4)) + (rhoCp*((T_crt-T_air)/rm)))    # original equation
#crt_rabs = .78*((epsilon*sigma*(T_crtK**4)) + (rhoCp*((dT_mean)/rm_mean)))
#crt_rabs = .78*((epsilon*sigma*(Tcrt_cus**4)) + (rhoCp*((dT_mean)/rm_mean)))    # for custom ranges

crt_rabs_Tcrt = .78*((epsilon*sigma*(Tcrt_cus**4)) + (rhoCp*((dT_mean)/rm_mean)))    # for Tcrt
crt_rabs_Tcrt_both = .78*((epsilon*sigma*(Tcrt_cus**4)) + (rhoCp*((Tcrt_cus-Ta_mean)/rm_mean)))    # for Tcrt both
crt_rabs_Ta = .78*((epsilon*sigma*(Tcrt_mean**4)) + (rhoCp*((Tcrt_mean-Ta_cus)/rm_mean)))    # for Ta
crt_rabs_dT = .78*((epsilon*sigma*(Tcrt_mean**4)) + (rhoCp*((dT_cus)/rm_mean)))    # for dT
crt_rabs_ws = .78*((epsilon*sigma*(Tcrt_mean**4)) + (rhoCp*((dT_mean)/rm_ws_cus)))    # for ws
crt_rabs_rm = .78*((epsilon*sigma*(Tcrt_mean**4)) + (rhoCp*((dT_mean)/rm_cus)))    # for rm

######## Calculate some slopes #####################

# For Tcrt and Rcrt relationship
slope_Tcrt = (np.max(crt_rabs_Tcrt) - np.min(crt_rabs_Tcrt))/len(Tcrt_cus)
print ('Slope Rcrt/Tcrt:'), slope_Tcrt
slope_Tcrt_both = (np.max(crt_rabs_Tcrt_both) - np.min(crt_rabs_Tcrt_both))/20.0
print ('Slope Rcrt/Tcrt both:'), slope_Tcrt_both
slop_Ta = (np.min(crt_rabs_Ta) - np.max(crt_rabs_Ta))/20.0
print('Slope Ta:'), slop_Ta
slope_dT = (np.max(crt_rabs_dT) - np.min(crt_rabs_dT))/11.0
print ('Slope dT:'), slope_dT

cust=[]
for i in range(len(ws_cus)):
	if ws_cus[i] == 1.0:
		print rm_ws_cus[i]
print np.min(rm_ws_cus)


# Plotting
plt.figure()
#plt.scatter(ws_cus, rm_ws_cus)
plt.plot(ws_cus, rm_ws_cus)
plt.grid()
#plt.title('Sensitivity of R$_{crt}$ to T$_{a}$ ')
#plt.xlabel('$T$$_{crt}$ ($\degree$$C$)')
#plt.xlabel('$T_{crt}-T_a$ ($\degree$$C$)')
plt.xlabel('Wind Speed ($ms^{-1}$)')
#plt.xlabel('$r_m$ ($sm^{-1}$)')
#plt.ylabel('$R$$_{crt}$ ($W/m$$^2$)')
plt.ylabel('$r_m$ ($sm^{-1}$)')
plt.xlim(0, 10)
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/sensitivities/ws_rm.pdf', dpi=300)
#plt.show()
'''














