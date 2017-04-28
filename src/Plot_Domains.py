import sys
sys.modules[__name__].__dict__.clear()
# ================================ Importing the functions =====================================
from CCLM_OUTS import Plot_CCLM
import matplotlib.pyplot as plt
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
# ==============================================================================================

fig = plt.figure('1')
fig.set_size_inches(14, 10)
# ================================= NAMELIST ===================================================
NN=1000
SEAS='DJF'
shift = 5
Vari   = 'T_2M'
buf    = 20
name_2 = 'member_relax_3_big_00_T_2M_ts_splitseas_1990_1999_' + SEAS + '.nc'
PDF    = 'Stations.pdf'
Plot_CCLM(dir_mistral='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',name=name_2,bcolor='black',var='T_2M',flag='FALSE',color_map='TRUE', alph=1, grids='FALSE', grids_color='red', rand_obs='TRUE', NN=NN)
col =['k','r','b','g','m']
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',
                                            name=name_2,
                                            var='T_2M')

for i in [1,3]:
    direc  = i


    name_1 = 'member_relax_'+ str(direc) +'_big_0' + str(shift) +'_'+ Vari +'_ts_splitseas_1990_1999_' + SEAS + '.nc'


    # ==============================================================================================
    t_f, lat_f, lon_f, rlat_f, rlon_f =rdfm(dir='/work/bb1029/b324045/work5/0'+ str(direc) +'/member_relax_' + str(direc) + '_big_0' + str(shift) + '/post/',
                                            name=name_1,
                                            var='T_2M')


    plt.hlines(y=min(rlat_f), xmin=min(rlon_f), xmax=max(rlon_f), color=col[i],linestyles= 'dashed', linewidth=4, alpha = .6)
    plt.hlines(y=max(rlat_f), xmin=min(rlon_f), xmax=max(rlon_f), color=col[i],linestyles= 'dashed', linewidth=4, alpha = .6)
    plt.vlines(x=min(rlon_f), ymin=min(rlat_f), ymax=max(rlat_f), color=col[i],linestyles= 'dashed', linewidth=4, alpha = .6)
    plt.vlines(x=max(rlon_f), ymin=min(rlat_f), ymax=max(rlat_f), color=col[i],linestyles= 'dashed', linewidth=4, alpha = .6)



plt.hlines(y=min(rlat_o[buf:-buf]), xmin=min(rlon_o[buf:-buf]), xmax=max(rlon_o[buf:-buf]), color='black', linewidth=4)
plt.hlines(y=max(rlat_o[buf:-buf]), xmin=min(rlon_o[buf:-buf]), xmax=max(rlon_o[buf:-buf]), color='black', linewidth=4)
plt.vlines(x=min(rlon_o[buf:-buf]), ymin=min(rlat_o[buf:-buf]), ymax=max(rlat_o[buf:-buf]), color='black', linewidth=4)
plt.vlines(x=max(rlon_o[buf:-buf]), ymin=min(rlat_o[buf:-buf]), ymax=max(rlat_o[buf:-buf]), color='black', linewidth=4)
plt.savefig(PDF)
plt.close()

### http://eca.knmi.nl/download/ensembles/Haylock_et_al_2008.pdf