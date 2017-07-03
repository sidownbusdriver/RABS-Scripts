import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

# Read in the data
f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cut_MCOM_831.csv'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/rooftop_08312014.csv'
data = np.recfromtxt(f1, unpack=True, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data1 = np.recfromtxt(f2, unpack=True, dtype=None, names=True, delimiter=',')

# Constants
emiss = .90            # emissivity 
k = .0274              # thermal conductivity
dz = 1.6               # meters
Ca = 1010.0            # heat capacity of air
sigma = 5.67*10**-8    # Stefan-Boltzman constant
rhoCp = 1212.0         # volumetric heat capacity of air @ 20C

def r_a(ws):
	"""Calculates the resistance of air to sensible heat transfer (s/m). Uses wind
	speed (m/s)."""
	k = 22.2*10**-6   # thermal diffusivity of air (m^2/s)
	v = 1.55*10**-5   # kinematic viscosity of air (m^2/s)
	Pr = .71          # Prandtl number
	Re = (ws*.17)/v
	if Re < 4000.0:
		A = .683
		n = .466
	elif Re >= 4000.0 and Re < 40000.0:
		A = .193
		n = .618
	elif Re > 40000.0:
		A = .0266
		n = .805
	ra = .17/(A*(Re**n)*(Pr**.33)*k)
	return ra

time = data['TIMESTAMP']
#time = time[:510]
#Ta = data['AirTC_Avg']
Ta = data1['Temp']
#Ta = Ta[:510]
Ta_k = Ta+273.15
L_up = data['LDnCo_Avg']
#L_up = L_up[:510]
ws = data['WS_ms_Avg']
#ws = ws[:510]
#print ws
Qnet = data['Rn_Avg']
#Qnet = Qnet[:510]

# Longwave correction for park
#L_up = data['LDn_Avg']
#L_up = L_up + ((5.67*10**-8)*(Ta_k**4.0))

dates = [dt.datetime.strptime(t, '%Y-%m-%d %H:%M:%S') for t in time]

# Calculations                 
Ts = (L_up/(emiss*sigma))**.25      # surface temperature (K)
#print Ts-273.15
dT = Ts-Ta_k
print ('Mean dT:'), stats.nanmean(dT)
Qg = k*(dT/dz)                      # conduction
#print np.mean(Qg)

# Using resistance 
ra = []
for i in range(len(ws)):
	ra.append(r_a(ws[i]))
Qh = rhoCp*(dT/ra)           # sensible heat flux
print ('Qh average:'), stats.nanmean(Qh)

Qe = Qnet-Qh
print ('Qe average:'), stats.nanmean(Qe)
print ('Qnet average:'), stats.nanmean(Qnet)
print ('Qg:'), stats.nanmean(Qg)
'''
# Save data to a file
valid_data = np.column_stack((time, Qh, Qe, Qg, dT))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/energy_budget/tennis_new.csv', valid_data, fmt='%s', delimiter=',')

# Plotting
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, Qnet, label='Q$^*$', color='black')
plt.plot(dates, Qh, label='Q$_H$', color='red')
plt.plot(dates, Qe, label='Q$_E$', color='green')
plt.title('Surface Energy Budget Over Tennis Court')
plt.xlabel('Time')
plt.ylabel('W/m$^2$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/energy_budget/sfc_energy_tennis_new.pdf', dpi=300)
#plt.show()
'''
       





