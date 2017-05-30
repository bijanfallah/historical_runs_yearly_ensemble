import sys
sys.modules[__name__].__dict__.clear()
# ================================ Importing the functions =====================================
## TODO: check the code and make it fancier!!!
from CCLM_OUTS import Plot_CCLM
import matplotlib.pyplot as plt
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
from sklearn.metrics import mean_squared_error
import numpy as np
import cartopy.crs as ccrs
from numpy import genfromtxt
import os, glob
# ==============================================================================================
# ================================== functions =================================================
def plot_rmse_spread(PDF="name.pdf",vari="RMSE",VAL=np.zeros((10,10,10)),x=10,y=10,col = ['k', 'r', 'b', 'g', 'm']):
    Plot_CCLM(dir_mistral='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/', name=name_2, bcolor='black',
              var=Vari, flag='FALSE', color_map='TRUE', alph=1, grids='FALSE', grids_color='red', rand_obs='FALSE',
              NN=NN)


    if vari == "RMSE":
        v = np.linspace(0, .8, 9, endpoint=True)
    else:
        v = np.linspace(0, .8, 9, endpoint=True)

    if vari == "RMSE":
        cs = plt.contourf(lons_f1,lats_f1,VAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.terrain)
        cb = plt.colorbar(cs)
        cb.set_label('RMSE [K]', fontsize=20)
        cb.ax.tick_params(labelsize=20)
    else:
        if vari == "SPREAD":
            cs = plt.contourf(lons_f1, lats_f1, VAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.terrain)
            cb = plt.colorbar(cs)
            cb.set_label('SPREAD [K]', fontsize=20)
            cb.ax.tick_params(labelsize=20)


    plt.hlines(y=min(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]),
               color='black', linewidth=4)
    plt.hlines(y=max(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]),
               color='black', linewidth=4)
    plt.vlines(x=min(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]),
               color='black', linewidth=4)
    plt.vlines(x=max(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]),
               color='black', linewidth=4)
    plt.savefig(PDF)
    plt.close()


# ==============================================================================================
fig = plt.figure('1')
fig.set_size_inches(14, 10)
# ================================= NAMELIST ===================================================
NN=1000
SEAS='DJF'
#SEAS='JJA'
Vari   = 'T_2M'
#Vari   = 'TOT_PREC'
buffer=20
name_2 = 'member_relax_3_big_00_' + Vari + '_ts_splitseas_1990_1999_' + SEAS + '.nc'
PDF1    = 'ENSEMBLE_RMSE_' + SEAS + '_'+ Vari +'.pdf'
PDF2    = 'ENSEMBLE_SPREAD_' + SEAS + '_'+ Vari +'.pdf'
timesteps=10   # number of the seasons (years)
start_time=0
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/', # the observation (default run without shifting)
                                            name=name_2,
                                            var=Vari)

here = "/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/"
# ==============================================================================================
if not os.path.exists(here+"Trash"):
    os.makedirs(here+"Trash")

counter = 0
for kk in range(1,6):
    shift = kk

    for i in range(1,5):

        direc  = i
        if i == 3:                                           # northwest shift
            start_lon = (buffer + shift)
            start_lat = (buffer - shift)
        else:
            if i == 2:                                      # northeast shift
                start_lon = (buffer - shift)
                start_lat = (buffer - shift)
            else:
                if i == 1:                                  # southeast shift
                    start_lon = (buffer - shift)
                    start_lat = (buffer + shift)
                else:
                    start_lon = (buffer + shift)           # southwest shift
                    start_lat = (buffer + shift)


        dext_lon = t_o.shape[2] - (2 * buffer)
        dext_lat = t_o.shape[1] - (2 * buffer)

        name_1 = 'member_relax_'+ str(direc) +'_big_0' + str(shift) +'_'+ Vari +'_ts_splitseas_1990_1999_' + SEAS + '.nc'


        # ==============================================================================================
        t_f, lat_f, lon_f, rlat_f, rlon_f =rdfm(dir='/work/bb1029/b324045/work5/0'+ str(direc) +'/member_relax_' + str(direc) + '_big_0' + str(shift) + '/post/',
                                                name=name_1,
                                                var=Vari)


        forecast = t_f[start_time:timesteps, start_lat:start_lat + dext_lat, start_lon:start_lon + dext_lon]
        for pp in range(start_time,timesteps):
            np.savetxt(here+"Trash/Forecast_" + str(pp) +"_" + str(direc) + "_"+ str(shift) + "_" + SEAS + ".csv", np.squeeze(forecast[pp,:,:]), delimiter=",")

        obs = t_o[start_time:timesteps, buffer:buffer + dext_lat, buffer:buffer + dext_lon]
        RMSE=np.zeros((forecast.shape[1], forecast.shape[2]))

        lats_f1=lat_f[start_lat:start_lat + dext_lat, start_lon:start_lon + dext_lon]
        lons_f1=lon_f[start_lat:start_lat + dext_lat, start_lon:start_lon + dext_lon]
        #rlats_f1 = rlat_f[start_lat:start_lat + dext_lat, start_lon:start_lon + dext_lon]
        #rlons_f1 = rlon_f[start_lat:start_lat + dext_lat, start_lon:start_lon + dext_lon]
        rlats_f1 = rlat_f[start_lat:start_lat + dext_lat]
        rlons_f1 = rlon_f[start_lon:start_lon + dext_lon]


        print forecast.shape,rlats_f1.shape, rlons_f1.shape,'-------------------------------------------------------------------------'
        for ii in range(0,forecast.shape[1]):
            for jj in range(0,forecast.shape[2]):
                forecast_resh=np.squeeze(forecast[:,ii,jj])
                obs_resh=np.squeeze(obs[:,ii,jj])
                RMSE[ii,jj] = mean_squared_error(obs_resh, forecast_resh) ** 0.5


        np.savetxt(here+"Trash/RMSE_"+str(counter)+".csv", RMSE, delimiter=",")
        for rr in range(0,timesteps-start_time):
            np.savetxt(here+"Trash/SPREAD_"+ str(rr)+ "_" + str(counter)+".csv", np.squeeze(forecast[rr,:,:]), delimiter=",")

        counter = counter + 1




RMSE = np.zeros((forecast.shape[1],forecast.shape[2]))


for pp in range(0, 20):

    RMSE = RMSE + genfromtxt(here+"Trash/RMSE_" + str(pp) + ".csv", delimiter=',')

RMSE = RMSE / 20
SPREAD = np.zeros((20,forecast.shape[1],forecast.shape[2]))
SPREAD_final = np.zeros((forecast.shape[1],forecast.shape[2]))
dumm = np.zeros((forecast.shape[1],forecast.shape[2]))
summ = np.zeros((timesteps,forecast.shape[1],forecast.shape[2]))
for gg in range(0,timesteps-start_time): # finding the standard deviation between all members over each time and then averaging them over time:
    for dd in range(0,20):
        dumm = genfromtxt(here+"Trash/SPREAD_"+ str(gg) + "_"+ str(dd)+".csv", delimiter=',')
        SPREAD[dd,:,:] = dumm[:,:]
    #SPREAD_01 = SPREAD - SPREAD
    #for dd in range(0,20):
    #    SPREAD_01[dd,:,:] = np.squeeze(SPREAD[dd,:,:]) - np.squeeze(np.mean(SPREAD,0))
    summ[gg,:,:] = np.std(SPREAD,0)
    #print summ[gg,:,:],'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    np.savetxt(here+"Trash/SEASON_SPREAD"+ str(gg) +"_"  + SEAS + ".csv", np.squeeze(summ[gg,:,:]), delimiter=",")
SPREAD_final = np.mean(summ,0)
# SAVING SPREAD and MEAN Forecast STATE for ENSEMBLE at each time-step: =========================================================

for tt in range(timesteps-start_time):
    dumm2 = np.zeros((forecast.shape[1], forecast.shape[2]))
    for gg in range(1,5): # finding the standard deviation between all members over each time and then averaging them over time:
        for dd in range(1,6):
            dumm2 = dumm2 + genfromtxt(here+"Trash/Forecast_" + str(tt) +"_" + str(direc) + "_"+ str(shift) + "_" + SEAS + ".csv", delimiter=",")
    dumm2 = dumm2 / 20
    np.savetxt(here+"Trash/SEASON_MEAN" + str(tt) + "_" + SEAS + ".csv", dumm2, delimiter=",")# save each month's ensemble mean
np.savetxt(here+"Trash/LAT.csv", rlats_f1, delimiter=",")
np.savetxt(here+"Trash/LON.csv", rlons_f1, delimiter=",")
#=======================================================================================================================
# PLOTING ==============================================================================================================

plot_rmse_spread(PDF=here+'Trash/'+PDF1,vari="RMSE",VAL=RMSE,x=forecast.shape[1],y=forecast.shape[2])
plot_rmse_spread(PDF=here+'Trash/'+PDF2,vari="SPREAD",VAL=SPREAD_final,x=forecast.shape[1],y=forecast.shape[2])

#==================== DELETING ========================
for filename in glob.glob(here + "TEMP/Trash/SPREAD_*.csv"):
    os.remove(filename)


for filename in glob.glob(here + "TEMP/Trash/RMSE_*.csv"):
    os.remove(filename)

for filename in glob.glob(here + "TEMP/Trash/Forecast_*.csv"):
    os.remove(filename)

# ============ END DELETING  ===========================














### http://eca.knmi.nl/download/ensembles/Haylock_et_al_2008.pdf