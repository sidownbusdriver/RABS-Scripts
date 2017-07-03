import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats
import math

#A_cyl = 0.00329867228627

# Functions
def pressure(A):
	"""Calculates pressure (kPa) using only altitude"""
	P_0 = 101.3
	Pa = P_0 * np.exp(-A/8200.0)
	return Pa
	
def Acs(r):
	"""Calculates cross-secional area of a cylinder where r is the radius (m)"""
	A = .1*(2*r)
	return A

def Acyl(r, h):
	"""Calculates the outer surface area of a cylinder where r is radius (m)
	and h is height of cylinder (m)"""
	A = (2.0*np.pi*r*h) + (2.0*np.pi*(r**2))
	return A

def solar_dec(d):
	"""Calculates solar declination (degrees) where d is the day. Where d=1 is 
	January 1. """
	angle = math.radians(360.0*(d+10.0)/365.0) # converts to radians
	dec = -23.4 * np.cos(angle)
	return dec

def solar_ET(d):
	"""Calculates the equation of time for use in calcuating the zenith angle"""
	f = math.radians(279.575 + 0.9856 * d)
	f2 = math.radians(2.0*(279.575 + 0.9856 * d))
	f3 = math.radians(3.0*(279.575 + 0.9856 * d))
	f4 = math.radians(4.0*(279.575 + 0.9856 * d))
	ET = ((-104.7*np.sin(f)) + (596.2*np.sin(f2)) + (4.3*np.sin(f3)) - (12.7 * 
	np.sin(f4)) - (429.3*np.cos(f)) - (2.0*np.cos(f2)) + (19.3 * np.cos(f3))) / 3600.0
	return ET

def solar_zen(lat, d, t, corr):
	"""Calculates the cosine of the zenith angle based on the time of day, the 
	latitude of the site and the time of year. t is in hours ranging from 0 to 24.  
	d is the calender day with J = 1 at January 1. LC is the longitude correction 
	(+7.5 to -7.5 either side of standard meridian). Corr is time correction. Zenith
	angle is returned in radians"""
	LC = corr / 60.0
	ET = solar_ET(d)
	to = 12.0 - LC - ET
	dec = solar_dec(d)
	cos_z = (np.sin(math.radians(lat)) * np.sin(math.radians(dec))) + (np.cos(math.radians(lat))
	* np.cos(math.radians(dec)) * np.cos(math.radians(15.0*(t-to))))
	zen = np.arccos(cos_z) 
	return zen    # should return zen

def opt_m(A ,lat, d, t, corr):
	"""Calculates optical air mass number. A is altitude (m), d is day, t is time of day
	(0-23), corr depends on month. Equation 3 (Kenny et al. 2008)."""
	Pa = pressure(A)
	zen = solar_zen(lat, d, t, corr)
	m = Pa/(101.3*np.cos(zen))
	return m

def est_Kd(A ,lat, d, t, corr, tao):
	"""function is used to estimate incoming shortwave diffuse radiation under
	clear sky conditions with inputs A(alititude, m), lat(latitude, degrees),
	d (days, Jan 1 =1), t (time, 24 hours), tao atmospheric transmittance
	(0.6-0.75 under clear skies). Equation 4 (Kenny et al. 2008)"""
	K_0 = 1367.0 # solar constant
	m = opt_m(A ,lat, d, t, corr)
	zen = solar_zen(lat, d, t, corr)
	Kd = .3*(1-(tao**m))*K_0*np.cos(zen)
	return Kd

def est_Kp(A, lat, d, t, corr, tao):
	"""equation used to estimate the incoming solar radiation (under clear sky
	conditions) with inputs A (altitude), lat (latitude), d (day), t (hour)
	Atr, atmospheric transmittance under clear sky conditions (varies between 0.6 and 
	0.75 for clear days). Equation 2 (Kenny et al. 2008)."""
	K_0 = 1367.0 # solar constant
	m = opt_m(A ,lat, d, t, corr)
	Kp = K_0*(tao**m)
	return Kp

def est_Kb(A, lat, d, t, corr, tao):
	"""written to estimate the incoming shortwave beam radiation based on methods 
	proposed by Campbell and Norman (1998) pg 172. Kp is the incoming shorwave on a 
	surface perpendicular to the beam and zen is the zenith angle. Inputs A (altitude, m),
	lat = latitude, d is days with January 1st being 1,t is time in hours. Eqn 1 (Kenny 
	et al. 2008)."""
	zen = solar_zen(lat, d, t, corr)
	Kp = est_Kp(A ,lat, d, t, corr, tao)
	Kb = Kp*np.cos(zen)
	return Kb

def Kb_cnr(Kin, A, lat, d, t, corr, tao):
	"""Calculate incoming direct beam solar radiation using net radiometer. Inputs are 
	Kin (measured incoming solar radiation, W/m^2), A (altitude), lat (latitude), d (day), 
	t (hour), tao (transmissivity)."""
	m = opt_m(A ,lat, d, t, corr)
	Kb = Kin/(1.0 + ((.5*(1-(tao**m)))/(tao**m)))
	return Kb

def est_Kt(A ,lat, d, t, corr, tao):
	"""used to calculate the estimated total incoming solar radiation based on Campbell 
	and Norman, 1995 with inputs (A, altitude m Guelph =334), lat(latitude, degrees, 
	Guelph = 43.55), t (time in decimal 24h). Equation 6 Kenny et al. 2008."""
	Kb = est_Kb(A ,lat, d, t, corr, tao)
	Kd = est_Kd(A ,lat, d, t, corr, tao)
	Kt = Kb + Kd
	return Kt

def est_Kr(A ,lat, d, t, corr, tao, albedo_g):
	"""Calculates amount of reflected radiation (W/m^2). A is altitude (m), lat is latitude
	(degrees), d is is day with jan. 1 = 1, t is decimal time (24h), corr is monthly 
	correction to time, tao is transmissivity, and albedo_g is the albedo of the ground
	surface. Equation 5 (Kenny et al. 2008)."""
	Kt = est_Kt(A ,lat, d, t, corr, tao)
	Kr = albedo_g*Kt
	return Kr
	
def abs_Kb(Kp, lat, d, t, corr, r, skin_alb):
	"""Calculates total incoming direct beam radiaiton absorbed by a vertical cylinder (W). 
	A is altitude (m), late is latitude (degrees), d is day with Jan 1 =1, t is hour of 
	day, corr is monthly correction to time, tao is transmissivity, r is radius of 
	cylinder, skin_alb is skin albedo."""
	#Kp = est_Kp(A, lat, d, t, corr, tao)
	zen = solar_zen(lat, d, t, corr)
	A_cs = Acs(r)
	Kb_abs = (1.0-skin_alb)*Kp*(np.sin(zen))*A_cs
	return Kb_abs

def abs_Kd(Kd, skin_alb, r, h):
	"""Calculates diffuse radiation absorbed by a cylinder (W). Kd is diffuse radiation 
	(W/m^2), skin_alb is skin albedo, r is cylinder radius (m), h is cylinder height (m).
	"""
	#Kd = est_Kd(A, lat, d, t, corr, tao)
	A_cyl = Acyl(r, h)
	Kd_abs = .5*(1-skin_alb)*Kd*A_cyl
	return Kd_abs

def abs_La(La, r, h):
	"""Calculates atmospheric long-wave radiation absorbed by a cylinder (W). La is 
	measured atmospheric long-wave radiation (W/m^2), r is cylinder radius (m), and h is 
	cylinder height (m)."""
	eh = .95   # emissivity of a human
	A_cyl = Acyl(r, h)
	La_abs = .5*eh*La*A_cyl
	return La_abs

def abs_Lg(Lg, r, h):
	"""Calculates ground surface long-wave radiation absorbed by a cylinder (W). Lg is 
	measured upwelling long-wave radiation, r is cylinder radius (m), and h is cylinder 
	height (m)."""
	eh = .95   # emissivity of a human
	A_cyl = Acyl(r, h)
	Lg_abs = .5*eh*Lg*A_cyl
	return Lg_abs
	
def cnr_Kb(Kt, A ,lat, d, t, corr, tao):
	"""Calculates incoming direct shortwave beam radiation. Equation 9 in Kenny et al. 
	(2008). Kt is measured incoming solar radiation, A is elevation (m), lat is latitude 
	in degrees, d is day with jan. 1 = 1, t is hour (0-24), corr is monthly correction 
	to time, tao is atmospheric transmissivity."""
	m = opt_m(A ,lat, d, t, corr)
	denom = (.3*(1.0-(tao**m)))/(tao**m)
	Kb = Kt/(1+denom)
	return Kb

def cnr_Kp(Kt, A ,lat, d, t, corr, tao):
	"""Calculates direct beam radiation received on a surface perpendicular to beam. Kt 
	is measured incoming solar radiation, A is elevation (m), lat is latitude in degrees, 
	d is day with jan. 1 = 1, t is hour (0-24), corr is monthly correction to time, tao 
	is atmospheric transmissivity.""" 
	Kb = cnr_Kb(Kt, A ,lat, d, t, corr, tao)
	zen = solar_zen(lat, d, t, corr)
	Kp = Kb/np.cos(zen)
	return Kp

def cnr_abs_Kb(Kt, A, lat, d, t, corr, tao, r, skin_alb):
	"""Calculates total incoming direct beam radiaiton absorbed by a vertical cylinder (W). 
	A is altitude (m), late is latitude (degrees), d is day with Jan 1 =1, t is hour of 
	day, corr is monthly correction to time, tao is transmissivity, r is radius of 
	cylinder (m), skin_alb is skin albedo, Kt is total incoming solar radiation."""
	Kp = cnr_Kp(Kt, A ,lat, d, t, corr, tao)
	zen = solar_zen(lat, d, t, corr)
	A_cs = Acs(r)
	Kb_abs = (1-skin_alb)*Kp*np.sin(zen)*A_cs
	return Kb_abs
	
def abs_Kup(Kup, r, h, skin_alb):
	"""Calculates reflected solar radiation absorbed by a cylinder. Kup is measured 
	reflected solar radiation (W/m^2), r is radius of cylinder (m), h is cylinder height
	(m), skin_alb is the albedo of the cylinder."""
	A_cyl = Acyl(r, h)
	Kup_abs = Kup*(1.0-skin_alb)*.5*A_cyl
	return Kup_abs
	
def abs_Kin(Kin, r, h, skin_alb):
	"""Calculates amount of incoming solar radiation absorbed by a cylinder. Kup is 
	measured incoming solar radiation (W/m^2), r is radius of cylinder (m), h is cylinder 
	height (m), skin_alb is the albedo of the cylinder."""
	A_cyl = Acyl(r, h)
	Kin_abs = Kin*(1.0-skin_alb)*.5*A_cyl
	return Kin_abs
	
	
	
	
	
	
	
	
	
