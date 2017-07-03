import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

#### Call in the file
f1 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_629_30_backyard.dat'
f2 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_630_sand.dat'
f3 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_714_park.dat'
f4 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_806_asphalt.dat'
f5 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_807_school.dat'
f6 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_808_tennis.dat'
f7 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_824_concrete.dat'
f8 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_MCOM_826.dat'
f9 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_MCOM_831.dat'
f10 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_green1.dat'
f11 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_green2.dat'
f12 = '/Users/ahardin/Documents/Masters_Research/wx_station_data/wx_data_turf_901.dat'
data1 = np.recfromtxt(f1, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data2 = np.recfromtxt(f2, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data3 = np.recfromtxt(f3, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data4 = np.recfromtxt(f4, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data5 = np.recfromtxt(f5, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data6 = np.recfromtxt(f6, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data7 = np.recfromtxt(f7, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data8 = np.recfromtxt(f8, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data9 = np.recfromtxt(f9, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data10 = np.recfromtxt(f10, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data11 = np.recfromtxt(f11, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')
data12 = np.recfromtxt(f12, unpack=True, skip_header=1, dtype=None, names=True, delimiter=',', missing_values='"NAN"')

# Assign data names
back_crt = data1['Temp_C_Avg']
back_crt = back_crt[:510]
sand_crt = data2['Temp_C_Avg']
park_crt = data3['Temp_C_Avg']
asphalt_crt = data4['Temp_C_Avg']
school_crt = data5['Temp_C_Avg']
tennis_crt = data6['Temp_C_Avg']
concrete_crt = data7['Temp_C_Avg']
MCOM826_crt = data8['Temp_C_Avg']
MCOM831_crt = data9['Temp_C_Avg']
green1 = data10['Temp_C_Avg']
green902_crt = green1[:356]
green903_crt = green1[2724:3236]
green904_crt = data11['Temp_C_Avg']
green904_crt = green904_crt[108:620]
turf_crt = data12['Temp_C_Avg']

# Wind
ws_concrete = data7['WS_ms_Avg']
green11 = data10['WS_ms_Avg']
ws_green902 = green11[:356]
ws_green903 = green11[2724:3236]
green2 = data11['WS_ms_Avg']
ws_green904 = green2[108:620]
ws_turf = data12['WS_ms_Avg']

conws = np.mean(ws_concrete)
print ('Concrete WS:'), conws
ws902 = np.mean(ws_green902)
print ('Green Roof 9/02 WS:'), ws902
ws903 = np.mean(ws_green903)
print ('Green Roof 9/03 WS:'), ws903
ws904 = np.mean(ws_green904)
print ('Green Roof 9/04 WS:'), ws904
turf_ws = np.mean(ws_turf)
print ('Turf WS'), turf_ws

'''
# Compute average CRT temp
back_avg = np.mean(back_crt)
print ('Backyard:'), back_avg
sand = np.mean(sand_crt)
print ('Sand:'), sand
park = np.mean(park_crt)
print ('Park:'), park
asphalt = np.mean(asphalt_crt)
print ('Apshalt:'), asphalt
school = np.mean(school_crt)
print ('School:'), school
tennis = np.mean(tennis_crt)
print ('Tennis:'), tennis
concrete = np.mean(concrete_crt)
print ('Concrete:'), concrete
mcom826 = np.mean(MCOM826_crt)
print ('MCOM 8/26:'), mcom826
mcom831 = np.mean(MCOM831_crt)
print ('MCOM 8/31:'), mcom831
green902 = np.mean(green902_crt)
print ('Green Roof 9/02:'), green902
green903 = np.mean(green903_crt)
print ('Green ROof 9/03:'), green903
green904 = np.mean(green904_crt)
print ('Green Roof 9/04'), green904
turf = np.mean(turf_crt)
print ('Turf:'), turf
'''






















