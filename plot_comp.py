import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/cnr_Rabs_comp/cnr_comp_park.csv'
data = np.recfromtxt(f1, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')

date = data['Date']
R = data['R_cnr']
Kup = data['Kup']
Kin = data['Kin']
Lup = data['Lup']
Lin = data['Lin']

# Convert dates
dates = [dt.datetime.strptime(t, '"%Y-%m-%d %H:%M:%S"') for t in date]

# Calculate averages
Kup_avg = stats.nanmean(Kup)
print ('Average Kup:'), Kup_avg
Kin_avg = stats.nanmean(Kin)
print ('Average Kin:'), Kin_avg
Lup_avg = stats.nanmean(Lup)
print ('Average Lup:'), Lup_avg
Lin_avg = stats.nanmean(Lin)
print ('Average Lin:'), Lin_avg
Ravg = stats.nanmean(R)
print ('Average R_cnr:'), Ravg
print ('----------------------------')

# Calculate Percentages
Kup_per = (Kup_avg/Ravg)*100.0
print ('Percent Kup:'), Kup_per
Kin_per = (Kin_avg/Ravg)*100.0
print ('Percent Kin:'), Kin_per
Lup_per = (Lup_avg/Ravg)*100.0
print ('Percent Lup:'), Lup_per
Lin_per = (Lin_avg/Ravg)*100.0
print ('Percent Lin:'), Lin_per

# Plotting
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, R, color='black', label='R$_{abs}$')
plt.plot(dates, Kup, color='red', label='K$_b$')
plt.plot(dates, Kin, color='purple', label='K$_d$')
plt.plot(dates, Lup, color='blue', label='L$_a$')
plt.plot(dates, Lin, color='brown', label='L$_g$')
#plt.ylim(-5, 480)
plt.xlabel('Time')
plt.ylabel('W/m$^2$')
plt.title('Human Radiation Budget over Wet Grass')
#plt.legend(loc='upper center')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/cnr_rabs_comp/R_comp_park.png')

# Plotting
plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.plot(dates, R)
plt.xlabel('Time')
plt.ylabel('R$_{cnr}$ (W/m$^2$)')
plt.title('Radiation Absorbed by a Human Over Wet Grass')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('/Users/ahardin/Documents/Masters_Research/wx_station_data/figures/cnr_Rabs/cnr_rabs_park.png')
#plt.show()





