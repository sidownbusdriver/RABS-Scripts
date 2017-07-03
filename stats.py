import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
from sklearn.metrics import mean_squared_error

f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/crt_Rabs/crt_rabs_green_904.csv'
f2 = '/Users/ahardin/Documents/Journal_Articles/Rabs/new_cnr/cut_green_904_RABS_B.txt'
#f3 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/theory_Rabs/est_rabs_green_904.csv'

data = np.recfromtxt(f1, unpack=True, dtype=None, names=True, delimiter=',', missing_values='nan')
data2 = np.genfromtxt(f2)
#data3 = np.recfromtxt(f3, unpack=True, dtype=None, names=True, delimiter=',')
#print data2

crt_R = data['crt_Rabs']
net_R = data2
#est_R = data3['theory_Rabs']

# Calculate mean of both
avg_crt = stats.nanmean(crt_R)
avg_net = stats.nanmean(net_R)
#avg_est = stats.nanmean(est_R)
meanR = (avg_net+avg_crt)/2.0

# Calculate root mean square error (RMSE)
error = crt_R - net_R
error_sqr = error**2
rmse = np.sqrt(stats.nanmean(error_sqr))
#rmse = np.sqrt(mean_squared_error(crt_R, net_R))
percent_rmse = (rmse/meanR)*100.0

# Calculate mean bias error (MBE)
mbe = stats.nanmean(error)

# Calculate mean absolute deviation (MAD)
mad = stats.nanmean(np.abs(error))

print 'MBE:', mbe
print 'MAD:', mad
print 'RMSE:', rmse
print 'Percent RMSE:', percent_rmse


