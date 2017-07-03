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
f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_714_park.dat'
data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

time = data['TIMESTAMP']
s_up = data['SUp_Avg']   # downwelling
s_down = data['SDn_Avg'] # upwelling
#l_up = data['LUpCo_Avg'] # downwelling
#l_down = data['LDnCo_Avg'] # upwelling
albedo = data['Albedo_Avg']

# Correction for park, long_up+5.67e-8*cnr4_T_K^4
temp = data['AirTC_Avg']
tempK = temp + 273.15
l_up = data['LUp_Avg']
#print ('L_up:'), stats.nanmean(
l_up = l_up + ((5.67*10**-8)*(tempK**4.0))
#print ('L_down:'), stats.nanmean(l_up)
l_down = data['LDn_Avg']
l_down = l_down + ((5.67*10**-8)*(tempK**4.0))
#print ('L_up:'), stats.nanmean(l_down)
'''
time = time[108:620]
s_up = s_up[108:620]
s_down = s_down[108:620]
l_up = l_up[108:620]
l_down = l_down[108:620]
albedo = albedo[108:620]
'''
r = .005   # radius of cylinder
skin_alb = .39
h = .1     # height of cylinder
A_eff = .78   # effective radiation area factor
A_cyl = R.Acyl(r, h)

# Change dates to datetime object
dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in time]

# Calculate four components of Rcnr
Kup_abs = R.abs_Kup(s_down, r, h, skin_alb)
Kup_comp = (Kup_abs/A_cyl)*A_eff

Kin_abs = R.abs_Kin(s_up, r, h, skin_alb)
Kin_comp = (Kin_abs/A_cyl)*A_eff

Lup_abs = R.abs_Lg(l_down, r, h)
Lup_comp = (Lup_abs/A_cyl)*A_eff

Lin_abs = R.abs_La(l_up, r, h)
Lin_comp = (Lin_abs/A_cyl)*A_eff

# Calculate Rcnr
R_cnr = A_eff*((Kup_abs+Kin_abs+Lup_abs+Lin_abs)/A_cyl)
R_cnr_mean = stats.nanmean(R_cnr)
print R_cnr_mean
print np.max(R_cnr)

R_cnr_comp = Kup_comp+Kin_comp+Lup_comp+Lin_comp
print stats.nanmean(R_cnr_comp)

# Make file
valid_data = np.column_stack((time, R_cnr_comp, Kup_comp, Kin_comp, Lup_comp, Lin_comp))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs_comp/cnr_comp_park.csv', valid_data, fmt='%s', delimiter=',')

other_data = np.column_stack((time, R_cnr))
np.savetxt('/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs/cnr_corr_park.csv', other_data, fmt='%s', delimiter=',')









