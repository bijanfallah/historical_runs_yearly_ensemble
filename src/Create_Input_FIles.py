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
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator as RegInt
# Step 1:
# ========================================== NAMELIST ================================================
SEAS = "DJF"
# flag1=True
NN = 600  # number of observations
month_length = 10
members = 20

dir_to_ensemble = "/var/autofs/net/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/TEMP/Trash"
# month=0
# ====================================================================================================
First_Guess = np.zeros(NN * month_length)
First_Guess_err = np.zeros(NN * month_length)
for i in range(0, members):
    Obs = pd.read_csv('TEMP/Stations_DATA_' + str(i) + '.csv',header=None)
    Obs.columns = ['lon', 'lat', 'Vals', 'Vals_dirty', 'Time']
    LAT = pd.read_csv("TEMP/Trash/LAT.csv", header=None)
    LON = pd.read_csv("TEMP/Trash/LON.csv", header=None)
    print LAT.shape, LON.shape

    Interp_Vals = np.zeros((NN*month_length))
    Forecast_err = np.zeros((NN*month_length))
    # TODO: check the interpolation !!!!

    z = range(0, month_length)

    # print 'halalooya'
    #for i in range(0, month_length):
    #    points[:, 0] = np.zeros(NN) + i
    #    Interp_Vals[:, i] = my_interpolating_function(points)

    Forecast_3 = np.array(pd.read_csv('TEMP/Trash/SEASON_MEAN1' + '_' + SEAS + '.csv', header=None))
    Forecast_3d = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
    #print Forecast_3d.shape
    #Forecast_3d = Forecast_3d.reshape((month_length,89,95))
    for month in range(0, month_length):
        Forecast = pd.read_csv('TEMP/Trash/SEASON_MEAN' + str(month) + '_' + SEAS + '.csv', header=None)
        Forecast_3d[month,:,:] = Forecast
    my_interpolating_function = RegInt((np.array(z), np.squeeze(np.array(LAT), 1), np.squeeze(np.array(LON), 1)),
                                       Forecast_3d, method='nearest')
    print np.array(Forecast).shape, LAT.shape, LON.shape
        #print  type(Obs.lon), type(LON)
    points = np.zeros((NN, 3))
    points[:, 1] = Obs.lat[0:NN]
    points[:, 2] = Obs.lon[0:NN]

    for month in range(0, month_length):
        print month
        points[:, 0] = np.zeros(NN)+month
        print my_interpolating_function(np.array(points[200:350,:]))
        Interp_Vals[(month * NN):((month * NN) + NN)] = my_interpolating_function(points)
        #First_Guess[(month * NN):((month * NN) + NN)] = Interp_Vals
        Forecast_err[(month * NN):((month * NN) + NN)] = pd.read_csv('TEMP/Trash/SEASON_SPREAD' + str(month) + '_' + SEAS + '.csv', header=None)



    #my_interpolating_function = interpolate.interp2d(np.array(LON), np.array(LAT), np.array(Forecast)[:, 0:-1])
    #print np.array(z).shape,LAT.shape,LON.shape, '_', Forecast_3d.shape



    #my_interpolating_function_2 = interpolate.interp2d(LON, LAT, np.array(Forecast_err)[:, :])
    #Interp_Vals_err = my_interpolating_function_2(Obs.lon[0:NN], Obs.lat[0:NN])
    #print Interp_Vals.shape

    #First_Guess_err[(month * NN):((month * NN) + NN)] = Interp_Vals_err

    from itertools import izip
    from itertools import repeat

    with open('TEMP/Trash/First_Guess_DATA_' + str(i) + '_.csv', 'wb') as f:
        writer = csv.writer(f)
        for ik in range(0, month_length):
            writer.writerows(izip(Obs.lon[0:NN], Obs.lon[0:NN], Interp_Vals, Forecast_err, list(repeat(ik, NN))))

    FG = pd.read_csv('TEMP/Trash/First_Guess_DATA_' + str(i) + '_.csv',header=None)
    FG.columns = ['lon', 'lat', 'Vals', 'Vals_err', 'Time']
    #### STEP  1

    f = Obs - Obs
    f.Vals = Obs.Vals_dirty - FG.Vals
    f.lon = Obs.lon
    f.lat = Obs.lat
    f.Time = Obs.Time

    #### Step  2


    Vari = np.zeros(month_length)
    for kkk in range(0, month_length):
        ER_Obs = Obs.Vals_dirty[Obs.Time == kkk] - Obs.Vals[Obs.Time == kkk]
        ER_BK = FG.Vals_err[Obs.Time == kkk]
        Vari[kkk] = np.var(ER_Obs) / np.var(ER_BK)

    ## Step 3 write the INPUT files:
    # write the x,y,f,var to the INPUT file
    import os

    ddd = os.getcwd()
    print ddd
    import csv
    from itertools import izip
    from itertools import repeat

    with open('INPUT' + str(i) + '.csv', 'wb') as ff:
        writer = csv.writer(ff)
        for ii in range(0, month_length):
            writer.writerows(izip(f.lon[f.Time == ii], f.lat[f.Time == ii], f.Vals[f.Time == ii]
                                  , f.Time[f.Time == ii], list(repeat(Vari[ii], NN))))

    # Write the grids for forecast domain :

    xv, yv = np.meshgrid(LON, LON, sparse=False, indexing='ij')
    np.savetxt('LON.out', xv, delimiter=',')
    np.savetxt('LAT.out', yv, delimiter=',')
    leng = LON.__len__() * LAT.__len__()
    lons = xv.reshape(leng, 1)
    lats = yv.reshape(leng, 1)

    with open('GRIDS.csv', 'wb') as gr:
        writer = csv.writer(gr)
        for ij in range(0, leng):
            writer.writerows(izip(lons[ij], lats[ij]))
