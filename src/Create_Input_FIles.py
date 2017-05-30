'''
This is the Program to create the INPUT files for the IO Program

Step 1 :  create the f (difference between background and the observation):
d=y^o - Hx^b

Step 2 : calculate the error variance of the observations divided by the
error variance of the background field
The mean state is the ensemble mean 
The variance is calculated from the ensemble

'''
import numpy as np
import csv
import pandas as pd
from scipy.interpolate import RegularGridInterpolator as RegInt
from itertools import izip
from itertools import repeat
import os
# Step 1:
# ========================================== NAMELIST ================================================

SEAS = "DJF"
NN=1000#number of observations
month_length=20
members=20
dir_to_ensemble = "/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/"
inflation=1.0
# ====================================================================================================

for i in range(0, members):
    Obs = pd.read_csv(dir_to_ensemble+'Trash/Stations_DATA_' + str(i) + '.csv',header=None)
    Obs.columns = ['lon', 'lat', 'Vals', 'Vals_dirty', 'Time']
    LAT = pd.read_csv(dir_to_ensemble+"Trash/LAT.csv", header=None)
    LON = pd.read_csv(dir_to_ensemble+"Trash/LON.csv", header=None)
    Interp_Vals = np.zeros((NN*month_length))
    Interp_errs = np.zeros((NN*month_length))
    Forecast_err = np.zeros((NN*month_length))
    z = range(0, month_length)
    Forecast_3 = np.array(pd.read_csv(dir_to_ensemble+'Trash/SEASON_MEAN1' + '_' + SEAS + '.csv', header=None))
    Forecast_3d = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
    Forecast_3d_err = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
    for month in range(0, month_length):
        Forecast_3d[month,:,:] = pd.read_csv(dir_to_ensemble+'Trash/SEASON_MEAN' + str(month) + '_' + SEAS + '.csv', header=None)
        Forecast_3d_err[month,:,:]= pd.read_csv(dir_to_ensemble+'Trash/SEASON_SPREAD' + str(month) + '_' + SEAS + '.csv', header=None)

    my_interpolating_function = RegInt((np.array(z), np.squeeze(np.array(LAT), 1), np.squeeze(np.array(LON), 1)),
                                       Forecast_3d, method='nearest')#Interpolating the Forecast mean on observations' location
    my_interpolating_function_2 = RegInt((np.array(z), np.squeeze(np.array(LAT), 1), np.squeeze(np.array(LON), 1)),
                                       Forecast_3d_err, method='nearest')#Interpolating the Forecast variance on observations' location
    
    points = np.zeros((NN, 3))
    points[:, 1] = Obs.lat[0:NN]
    points[:, 2] = Obs.lon[0:NN]

    for month in range(0, month_length):
        points[:, 0] = np.zeros(NN)+month
        Interp_Vals[(month * NN):((month * NN) + NN)] = my_interpolating_function(points)
        Interp_errs[(month * NN):((month * NN) + NN)] = my_interpolating_function_2(points)

    with open(dir_to_ensemble+'Trash/First_Guess_DATA_' + str(i) + '_.csv', 'wb') as f:
        writer = csv.writer(f)
        for ik in range(0, month_length):
            writer.writerows(izip(Obs.lon[0:NN], Obs.lon[0:NN], Interp_Vals[(ik * NN):((ik * NN) + NN)]
                                  , Interp_errs[(ik * NN):((ik * NN) + NN)], list(repeat(ik, NN))))

    FG = pd.read_csv(dir_to_ensemble+'Trash/First_Guess_DATA_' + str(i) + '_.csv',header=None)
    FG.columns = ['lon', 'lat', 'Vals', 'Vals_err', 'Time']

    #### STEP  1
    f = Obs - Obs
    f.Vals = Obs.Vals_dirty - FG.Vals
    f.lon = Obs.lon
    f.lat = Obs.lat
    f.Time = Obs.Time

    #### Step  2
    Vari = np.zeros(NN)
    #for kkk in range(0, month_length):
    #    ER_Obs = Obs.Vals_dirty[Obs.Time == kkk] - Obs.Vals[Obs.Time == kkk]
    #    ER_BK = FG.Vals_err[Obs.Time == kkk]
    #    Vari[kkk] = np.var(ER_Obs) / 100*np.var(ER_BK)#TODO: calculate this for each gridpoint!!!!! and insert in line 94 instead of repeating!!!!!!!!!
        #Vari[kkk,NN] = np.var(ER_Obs) / 100*np.var(ER_BK)
        #print np.var(ER_BK)
    ER_Obs = np.zeros(NN)
    ER_BK = np.zeros(NN)
    for mm in range(0,NN):
        indxs = np.arange(mm,(NN*month_length)+1,NN)

        ER_Obs[mm] = np.var(Obs.Vals_dirty[indxs]-Obs.Vals[indxs])
        ER_BK[mm]  =  np.mean(FG.Vals_err[indxs])*inflation #inflation
        #print FG.Vals_err[indxs]
        #print '--------------------------------------------------------'
        #print 'pay attention!!!!!!!!!!!!!!!!!!!!!',ER_Obs[mm],ER_BK[mm]
        #print '--------------------------------------------------------'
    Vari = ER_Obs / ER_BK





    ## Step 3 write the INPUT files:
    # write the x,y,f,var to the INPUT file

    ddd = os.getcwd()
    print ddd


    with open(dir_to_ensemble+'INPUT' + str(i) + '.csv', 'wb') as ff:
        writer = csv.writer(ff)
        for ii in range(0, month_length):
            #writer.writerows(izip(f.lon[f.Time == ii], f.lat[f.Time == ii], f.Vals[f.Time == ii]
            #                      , f.Time[f.Time == ii], list(repeat(Vari[ii], NN))))
            writer.writerows(izip(f.lon[f.Time == ii], f.lat[f.Time == ii], f.Vals[f.Time == ii]
                                  , f.Time[f.Time == ii], list(Vari)))


    # Write the grids for forecast domain :

    xv, yv = np.meshgrid(LON, LAT, sparse=False, indexing='ij')
    np.savetxt(dir_to_ensemble+'LON.out', xv, delimiter=',')
    np.savetxt(dir_to_ensemble+'LAT.out', yv, delimiter=',')
    leng = LON.__len__() * LAT.__len__()
    lons = xv.reshape(leng, 1)
    lats = yv.reshape(leng, 1)

    with open(dir_to_ensemble+'GRIDS.csv', 'wb') as gr:
        writer = csv.writer(gr)
        for ij in range(0, leng):
            writer.writerows(izip(lons[ij], lats[ij]))
