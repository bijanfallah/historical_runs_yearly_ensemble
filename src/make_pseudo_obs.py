def extract_pseudo(NN=2000,dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',
                   name='member_relax_3_big_00_T_2M_ts_splitseas_1990_1999_DJF.nc',var='T_2M',month_length=20, buffer = 20):

    '''
    :param nn: number of observations, no: number of members
    :return: PO, lon, lat, rlon, rlat pseudo obs and their locations in rotated and regular grid
    '''
    #import math
    import numpy as np
    import matplotlib.pyplot as plt
    #import random
    #import scipy.spatial as spatial
    #random.seed(770)
    from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
    from CCLM_OUTS import rand_station_locations as rsl
    s, t = rsl(N=7000, sed=770)
    #TT=t.values()
    TT=t
    #SS=s.values()
    SS=s
    from rotgrid import Rotgrid

    mapping = Rotgrid(-165.0, 46.0, 0, 0)# TDOD: this line has to be adopted according to the CCLM domain!!!
    for i in range(0, NN):
       # print(t.values()[i])
        (TT[i], SS[i]) = mapping.transform(TT[i], SS[i])

    points=np.zeros((NN,3))
    #TODO: data-thining
    # thin the data to let one obs in each grid:
    #fert_ok = 0
    poi = np.array([SS[0:NN], TT[0:NN]])
    print poi.shape
    #point_tree = spatial.cKDTree(np.transpose(poi))
    #for fert in range(NN):


    #    if len(point_tree.query_ball_point([SS[fert],TT[fert]], .44)) >= 1:

    #        print len(point_tree.query_ball_point([SS[fert],TT[fert]], .44)), fert_ok
    #        points[fert_ok, 1] = SS[fert]
    #        points[fert_ok, 2] = TT[fert]
    #        fert_ok = fert_ok + 1
    points[:, 1] = SS[0:NN]
    points[:, 2] = TT[0:NN]

    t_o, lat_o, lon_o, rlat_o, rlon_o = rdfm(dir, name, var)




    #print(t_o.shape)
    Interp_Vals=np.zeros((NN,month_length))
    Interp_Vals_dirty=np.zeros((NN,month_length))
    noise=np.zeros((NN,month_length))
    from scipy.interpolate import RegularGridInterpolator as RegInt
    z=range(0,month_length)
    my_interpolating_function = RegInt((z,rlat_o[buffer:-buffer], rlon_o[buffer:-buffer]), t_o[0:month_length,buffer:-buffer,buffer:-buffer], method='nearest')

    #print 'halalooya'
    for i in range(0,month_length):
        points[:, 0] = np.zeros(NN)+i
        Interp_Vals[:,i] = my_interpolating_function(points)
    #for jjj in range(0,no):

    for k in range(0,NN):
        #np.random.seed(777+k)
        #noise[k,:] = np.random.normal(0, np.sqrt(np.var(Interp_Vals[k,:])/200), 12)
        #noise[k,:] = np.random.normal(0, .3, month_length) # for monthly values
        #noise[k,:] = np.random.normal(0, .5, month_length) # for sesonal values T_2M winter DJF
        noise[k,:] = np.random.normal(0, .3, month_length) # for sesonal values T_2M summer JJA
        #noise[k,:] = np.random.normal(0, .1, month_length) # for sesonal values TOT_PREC

        # plt.hist(f,30) to plot the noise


        Interp_Vals_dirty[k,:] = Interp_Vals[k,:] + noise[k,:]

    #fig = plt.figure('3')
    #fig.set_size_inches(14, 10)
    #noi = np.random.normal(0, .5, 30)
    #print 'SNR = =================',((0.5**2) / np.mean(noi**2))
    #plt.hist(noi, bins=10)
    #plt.title('Example of added error for a single point', size=30, y=1.02)
    #plt.xlabel('$Error (K)$', size=30)
    #plt.savefig('NOISE.pdf')
    #plt.close()
    return(Interp_Vals_dirty, Interp_Vals, TT[0:NN], SS[0:NN], t_o[0:month_length,:,:], rlon_o, rlat_o)

# ========================================= NAMELIST ===============================================
month_length=10
SEAS="DJF"
NN=600#Number of Observations
dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/'
name = 'member_relax_3_big_00_T_2M_ts_splitseas_1990_1999_' + SEAS + '.nc'
NO=20  # number of ensemble members
buffer=20
dir_to_ensemble = "/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly_ensemble/src/"
# ==================================================================================================

# Programs body
import numpy as np
for jj in range(0,NO):


    Temp_Station_dirty, Temp_Station, rlon_s, rlat_s, t_o , rlon_o, rlat_o=extract_pseudo(NN, dir, name=name, month_length=month_length)

    #for checking put flag='TRUE'
    flag=False

    if flag==True:
        import matplotlib.pyplot as plt
        plt.contourf(rlon_o, rlat_o, t_o[1, :, :]-273,100,cmap='jet', vmin=-10, vmax=20)
        plt.colorbar()
        plt.scatter(rlon_s, rlat_s, c=np.squeeze(Temp_Station_dirty[:,1])-273, cmap='jet', s=50, vmin=-10, vmax=20)
        plt.show()


    if flag==True:
        import matplotlib.pyplot as plt
        #plt.contourf(rlon_o, rlat_o, t_o[1, :, :]-273,100,cmap='jet', vmin=-10, vmax=20)
        #plt.colorbar()
        s=np.power(Temp_Station_dirty[:, 1] - Temp_Station[:, 1], 2)
        s=np.sqrt(s)
        plt.scatter(rlon_s, rlat_s, c=np.squeeze(s), cmap='jet', s=50, vmin=0, vmax=2)
        plt.colorbar()
        plt.show()


    import csv
    from itertools import izip
    from itertools import repeat
    with open(dir_to_ensemble + 'Trash/Stations_DATA_' + str(jj) + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0, month_length):
            writer.writerows(izip(rlon_s,rlat_s,Temp_Station[:,i],Temp_Station_dirty[:,i],list(repeat(i,NN))))





