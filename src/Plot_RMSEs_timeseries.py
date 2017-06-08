# Program to plot the RMSEs time-series of Forecast quantities for each member
# ------------------------ Import----------------------------------------------
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import sem
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
# -----------------------------------------------------------------------------

# ------------------------ Namelist -------------------------------------------

NN=1000
SEAS='DJF'
#SEAS='JJA'
Vari   = 'T_2M'
#Vari   = 'TOT_PREC'
month_length=20   # number of the seasons (years)
start_time=0
here = "/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/"
no_members=20
buffer=20
# -----------------------------------------------------------------------------
name_2 = 'member_relax_3_big_00_' + Vari + '_ts_splitseas_1990_1999_' + SEAS + '.nc'
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/', # the observation (default run without shifting)
                                            name=name_2,
                                            var=Vari)

forecast = genfromtxt(here+'NAMES'+'/'+"Trash/Forecast_0_1_1_" + SEAS + ".csv", delimiter=",")
dumm2 = np.zeros((forecast.shape[0], forecast.shape[1]))
time_series = np.zeros((month_length,no_members))
time_series_min    = np.zeros(month_length)
time_series_max    = np.zeros(month_length)
time_series_mean   = np.zeros(month_length)
time_series_Nature = np.zeros(month_length)
for ii in range(0,month_length):
    counter = 0
    for kk in range(1,5):
        for jj in range(1,6):
            if counter < no_members:
                dumm2 = genfromtxt(here+'NAMES'+'/'+"Trash/Forecast_" + str(ii) +"_" + str(kk) + "_"+ str(jj) + "_" + SEAS + ".csv", delimiter=",")
                time_series[ii,counter] = np.mean(dumm2)
            counter = counter + 1
dext_lon = t_o.shape[2] - (2 * buffer)
dext_lat = t_o.shape[1] - (2 * buffer)

time_series_Nature = np.mean(t_o[:,buffer:buffer + dext_lat, buffer:buffer + dext_lon],axis=(1,2))

time = range(1,month_length+1)
time_series_mean = np.mean(time_series,1)
time_series_max  = np.max(time_series,1)
time_series_min  = np.min(time_series,1)

# ------------ ploting -------------------------------------------------------

fig = plt.figure(111)
fig.set_size_inches(14, 10)
plt.fill_between(time, time_series_max,
                 time_series_min, color="#3F5D7D")
plt.plot(time, time_series_mean, color="white", lw=2)
plt.plot(time, time_series_Nature, color="red", lw=2)
plt.xlabel("Time", fontsize=10)
plt.ylabel(Vari, fontsize=10)
plt.savefig(here+'/final_plot/'+"Time_series_"+Vari+'_'+SEAS+".pdf", bbox_inches="tight");
plt.close()
