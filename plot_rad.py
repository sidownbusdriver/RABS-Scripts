import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_turf_901.dat'
data = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

# Data
record = data['RECORD']
s_up = data['SUp_Avg']   # downwelling
s_down = data['SDn_Avg'] # upwelling
l_up = data['LUpCo_Avg'] # downwelling
l_down = data['LDnCo_Avg'] # upwelling
net = data['Rn_Avg']
'''
# Plotting for backyard
plt.figure()
plt.plot(record[108:620], s_up[108:620], 'blue', label='$K\downarrow$')
plt.plot(record[108:620], s_down[108:620], 'red', label='$K\uparrow$')
plt.plot(record[108:620], l_up[108:620], 'green', label='$L\downarrow$')
plt.plot(record[108:620], l_down[108:620], 'brown', label='$L\uparrow$')
plt.plot(record[108:620], net[108:620], 'black', label='$Q^*$')
lgd = plt.legend(loc='center', bbox_to_anchor=(0.5,-0.1), ncol=5)
plt.title('Radiation Budget over Green Roof 9/04')
plt.xlabel('timestep')
plt.ylabel('$W/m^2$')
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/radiation/greenroof_904_rad.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
'''
# Plot others
plt.figure()
plt.plot(record, s_up, 'blue', label='$K\downarrow$')
plt.plot(record, s_down, 'red', label='$K\uparrow$')
plt.plot(record, l_up, 'green', label='$L\downarrow$')
plt.plot(record, l_down, 'brown', label='$L\uparrow$')
plt.plot(record, net, 'black', label='$Q^*$')
lgd = plt.legend(loc='center', bbox_to_anchor=(0.5,-0.1), ncol=5)
plt.title('Radiation Budget over Turf')
plt.xlabel('timestep')
plt.ylabel('$W/m^2$')
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/radiation/turf_rad.png', bbox_extra_artists=(lgd,), bbox_inches='tight')






