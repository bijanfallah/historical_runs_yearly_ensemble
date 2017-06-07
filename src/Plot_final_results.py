# This is a program to plot:
# 1- maps of RMSEs for the ensemble analysis
# 2- boxplot of RMSEs for Forecast vs Analysis
# ------------------------- Imports ----------------------------
import csv
from itertools import izip
import pandas as pd
import csv
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from CCLM_OUTS import Plot_CCLM
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm

# --------------------------------------------------------------
# ------------------------- Namelist ---------------------------
SEAS='DJF'
NN=1000#number of observations should be read from previous funcions!!!!
month_length=20
SEAS='DJF'
Vari   = 'T_2M'
buffer=20
timesteps=10   # number of the seasons (years)
start_time=0
name_2 = 'member_relax_3_big_00_' + Vari + '_ts_splitseas_1990_1999_' + SEAS + '.nc'
DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/Optimal_Interpolation/optiminterp/inst/'
DIR_exp="/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/"
no_members=20
inflation=1.1 #NEW variable!!!!
# --------------------------------------------------------------
LAT = pd.read_csv(DIR_exp+'NAMES'+'/'+"Trash/LAT.csv", header=None)
LON = pd.read_csv(DIR_exp+'NAMES'+'/'+"Trash/LON.csv", header=None)
Forecast_3 = np.array(pd.read_csv(DIR_exp+'NAMES'+'/'+'Trash/SEASON_MEAN1' + '_' + SEAS + '.csv', header=None))#Reading the Forecast values
t_f = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
for month in range(0, month_length):# Reading the ensemble forecast for each month!
    t_f[month,:,:] = pd.read_csv(DIR_exp+'NAMES'+'/'+'Trash/SEASON_MEAN' + str(month) + '_' + SEAS + '.csv', header=None)
t_f = np.array(t_f)
## add correction to forecast :
# declare zero matrix which will be filled
result_IO = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))

for i in range(0,month_length):
    result = np.zeros((Forecast_3.shape[0], Forecast_3.shape[1]))
    for member in range(0,no_members):
        fil='333333'+ str(member)+'_' + str(inflation)+'_'+str(member)+'/optiminterp/inst/' + 'fi' + str(no_members) + str(i) +'.csv'
        result=result + np.array(list(csv.reader(open(fil,"rb"),delimiter=','))).astype('float')
        
    result_IO[i,:,:] = np.squeeze(t_f[i,:,:]) + (result/no_members)
   
# plot the ensemble Analysis RMSE :

pdf_name='Ensemble_RMSE_last_m100_l20.pdf'
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',
                                        name=name_2,
                                        var=Vari)
dext_lon = t_o.shape[2] - (2 * buffer)
dext_lat = t_o.shape[1] - (2 * buffer)
start_lon=(buffer+4)
start_lat=(buffer-4)
forecast = result_IO
obs = t_o[0:month_length, buffer:buffer + dext_lat, buffer:buffer + dext_lon]
RMSE=np.zeros((forecast.shape[1],forecast.shape[2]))
RMSE_TIME_SERIES=np.zeros(forecast.shape[0])
RMSE_TIME_SERIES_Forecast=np.zeros(forecast.shape[0])
for i in range(0,forecast.shape[1]):
    for j in range(0,forecast.shape[2]):
        forecast_resh=np.squeeze(forecast[:,i,j])
        obs_resh=np.squeeze(obs[:,i,j])
        RMSE[i,j] = mean_squared_error(obs_resh, forecast_resh) ** 0.5 # Calculating the RMSEs for each grid point

for i in range(0,forecast.shape[0]):
    forecast_resh_ts=np.squeeze(forecast[i,:,:])
    obs_resh_ts=np.squeeze(obs[i,:,:])
    RMSE_TIME_SERIES[i] = mean_squared_error(obs_resh_ts, forecast_resh_ts) ** 0.5 #Calculating RMSEs for each month for Analysis


for i in range(0,forecast.shape[0]):
    forecast_orig_ts=np.squeeze(t_f[i,:,:])
    obs_resh_ts=np.squeeze(obs[i,:,:])
    RMSE_TIME_SERIES_Forecast[i] = mean_squared_error(obs_resh_ts, forecast_orig_ts) ** 0.5 #Calculating RMSEs for each month for forecast
## Plotting core :

fig = plt.figure('1')
fig.set_size_inches(14, 10)

rp = ccrs.RotatedPole(pole_longitude=-165.0,# this number comes from int2clm settings
                          pole_latitude=46.0,# this number comes from int2clm settings
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))
pc = ccrs.PlateCarree()
ax = plt.axes(projection=rp)
ax.coastlines('50m', linewidth=0.8)
if SEAS[0] == "D":
    v = np.linspace(0, .8, 9, endpoint=True)# the limits of the colorbar for winter
else:
    v = np.linspace(0, .8, 9, endpoint=True)# the limits of the colorbar for other seasons

# Write the RMSE mean of the member in a file

names=DIR_exp+'RMSE_'+pdf_name+'.csv'
with open(names, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow([NN,np.mean(RMSE)])
     
lats_f1=lat_o[buffer:buffer + dext_lat, buffer:buffer + dext_lon]
lons_f1=lon_o[buffer:buffer + dext_lat, buffer:buffer + dext_lon]
cs=plt.contourf(lons_f1, lats_f1, RMSE,v, transform=ccrs.PlateCarree(), cmap=plt.cm.terrain)
cb = plt.colorbar(cs)
cb.set_label('RMSE [K]', fontsize=20)
cb.ax.tick_params(labelsize=20)
ax.gridlines()
ax.text(-45.14, 15.24, r'$45\degree N$',
        fontsize=15)
ax.text(-45.14, 35.73, r'$60\degree N$',
        fontsize=15)
ax.text(-45.14, -3.73, r'$30\degree N$',
        fontsize=15)
ax.text(-45.14, -20.73, r'$15\degree N$',
        fontsize=15)
ax.text(-19.83, -35.69, r'$0\degree $',
        fontsize=15)
ax.text(15.106, -35.69, r'$20\degree E$',
        fontsize=15)
        
plt.hlines(y=min(rlat_o), xmin=min(rlon_o), xmax=max(rlon_o), color='black',linestyles= 'dashed', linewidth=2)
plt.hlines(y=max(rlat_o), xmin=min(rlon_o), xmax=max(rlon_o), color='black',linestyles= 'dashed', linewidth=2)
plt.vlines(x=min(rlon_o), ymin=min(rlat_o), ymax=max(rlat_o), color='black',linestyles= 'dashed', linewidth=2)
plt.vlines(x=max(rlon_o), ymin=min(rlat_o), ymax=max(rlat_o), color='black',linestyles= 'dashed', linewidth=2)
plt.hlines(y=min(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]), color='black', linewidth=4)
plt.hlines(y=max(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]), color='black', linewidth=4)
plt.vlines(x=min(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]), color='black', linewidth=4)
plt.vlines(x=max(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]), color='black', linewidth=4)
Plot_CCLM(dir_mistral='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',name=name_2,bcolor='black',var=Vari,flag='FALSE',color_map='TRUE', alph=1, grids='FALSE', grids_color='red', rand_obs='TRUE', NN=NN)
xs, ys, zs = rp.transform_points(pc,
                                 np.array([-17, 105.0]),# Adjust for other domains!
                                 np.array([3, 60])).T   # Adjust for other domains!
ax.set_xlim(xs)
ax.set_ylim(ys)
plt.savefig(DIR_exp+pdf_name)
plt.close()

# RMSE time-series

fig = plt.figure('2')
fig.set_size_inches(14, 10)
plt.ylabel('$RMSE$', size=35)
plt.title('Boxplot of seasonal RMSEs averaged over the domain', size=30 , y=1.02)
#plt.ylim([0,.45])

names=DIR_exp+pdf_name+'_Analysis.csv'
with open(names, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow(RMSE_TIME_SERIES)

plt.boxplot([RMSE_TIME_SERIES,RMSE_TIME_SERIES_Forecast.transpose(), ])
plt.xticks([1, 2], ['$Analysis$', '$Forecast$'], size=35)
plt.savefig(DIR_exp+pdf_name+'_ts.pdf')
plt.close()


