import sys
sys.modules[__name__].__dict__.clear()
from CCLM_OUTS import Plot_CCLM
import matplotlib.pyplot as plt
fig = plt.figure('1')
fig.set_size_inches(14, 10)
# ================================= NAMELIST ===================================================
NN=1000
SEAS='DJF'
name_2 = 'member_relax_3_big_00_T_2M_ts_splitseas_1990_1999_' + SEAS + '.nc'
PDF    = 'Stations.pdf'
# ==============================================================================================

Plot_CCLM(dir_mistral='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/',name=name_2,bcolor='red',var='T_2M',flag='FALSE',color_map='TRUE', alph=1, grids='TRUE', grids_color='red', rand_obs='TRUE', NN=NN)
#Plot_CCLM(dir_mistral='3/',name=name_2,bcolor='red',var='T_2M',flag='FALSE',color_map='TRUE', alph=1, grids='TRUE', grids_color='red', rand_obs='TRUE', NN=NN)
plt.savefig(PDF)
plt.close()

### http://eca.knmi.nl/download/ensembles/Haylock_et_al_2008.pdf


