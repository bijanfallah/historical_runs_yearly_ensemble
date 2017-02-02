'''
Program to plot the changes of RMSE with respect to the changes in correlation length and number of observations
'''
# ============================== NAMELIST ======================================
MAX_L=50
month_length=30
SEAS="JJA"
NN=500
#COR_LEN=1
M=30 #Number of influential points
DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly/src/TEMP'
# ===============================================================================

pdf_name='RMSE_L_' + SEAS + '_' + str(month_length) + '_' + str(NN) + '_' + str(M) + '_' + '.pdf'
import numpy as np
import csv
import os
#res= np.zeros((16,50))
#res= np.zeros((7,50))
res= np.zeros((7,MAX_L))
k=0
#for i in range(500,2100,100):
print 'hello'
for i in range(500,600,100):
    kk=0
    for j in range(1,(MAX_L+1)):
        #if (j<10):
            #names=DIR+'/Second_RUN_'+str(j)+'_'+str(i)+'/TEMP/RMSE_last_m'+str(500+j)+'.pdf.csv'
        #    names = 'RMSE_last_m' + str(i + j) + '.pdf.csv'
        #else:
            #names=DIR+'/Second_RUN_'+str(j)+'_'+str(i)+'/TEMP/RMSE_last_m'+str(5000+j)+'.pdf.csv'
        #    names = 'RMSE_last_m' + str(i + j) + '.pdf.csv'
        names = 'TEMP/RMSE_last_m_' + SEAS + '_' + str(M) + '_' + str(j) + '_' + str(i) + '.pdf.csv'
        print(names)
        print 'hello'
        print os.getcwd()
        result = np.array(list(csv.reader(open(names, "rb"), delimiter=','))).astype('float')
        print(result)
        res[k,kk]=result[0,1]
        print(res[k,kk])
        print(k,kk)
        kk=kk+1
    k=k+1



import matplotlib.pyplot as plt

fig, ax = plt.subplots()
fig.set_size_inches(14, 10)
#for i in range(16):
x=range(1,(MAX_L + 1))
i=0
#for i in range(7):
#    ax.plot(x,res[i,:],'o-', label=str(i*100+500), lw=3, alpha=.7, ms=10)
#    ax.legend(loc='upper center', shadow=True)
ax.plot(x,res[i,:],'ko-', label=str(500), lw=3, ms=10, alpha=.5)
if SEAS == 'DJF':
    ax.plot(x[11],min(res[0,:]),'k*', label=str(500), lw=3,  ms=20) # DJF
else:
    ax.plot(x[2],min(res[0,:]),'k*', label=str(500), lw=3,  ms=20) # JJA

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_title("", y=1.05)
ax.set_ylabel(r"$RMSE$", labelpad=5,size=32)
ax.set_xlabel(r"$L$", labelpad=5,size=32)
#plt.legend(loc=4, shadow=True,fontsize=32)
plt.xlim(0,(MAX_L + 1))
#if SEAS == 'DJF':
 #   plt.ylim(0.6,1.4) #DJF
#else:
 #   plt.ylim(0.22,0.26) #JJA
plt.tick_params(axis='both', which='major', labelsize=22)
plt.savefig(pdf_name)