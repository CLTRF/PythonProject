#required setup
#mcu
#spectrum analyzer N9000A
#if generator


#P47-60
#RF freq 8250 fixed
#IF power fixed
#modcon vary
#plot spur levels as time20.0	30.0
#
#20.0	30.0
#P47-50
#RF freq 8250 fixed
#IF power fixed
#plot spur levels as time


import instruments as ik
import sys,os
sys.path.insert(1, '/home/max/python/myimport')
import numpy as np
import SMU200
import N9000A
import time
import json
import datetime
import select


#######################20.0	30.0#######################################################
#                           main program
##############################################################################

#TCP settings
N9000a_host='10.0.9.212'



#setup1 P47-10
LO_freq=3365 #error of pll setting #
#IF frequnecy
IF_freq=3022.5
time_nop=5
if_power=-20
myoffset=17 #need to be specified
mod_choice=0


#initalization of instruments
N9000b=N9000A.N9000(N9000a_host)


# RF frequnecy
RF_range=[3000,3100] #MHz

cal=True

if cal==True:
    N9000b.NF_meas(RF_range[0],RF_range[1],2,8,41)
    print("Do calibration, hit enter when ready to capture data ")
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = raw_input()
            break

for LNA_no in range(1,5):
    print("Connect cable to LNA{0} to Do measurements and hit ready to capture data ".format(LNA_no))
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = raw_input()
            break
    N9000b.copy_picture1("pic{0}".format(LNA_no))
    NF,Gain=list(N9000b.get_NF())
    xx="{0}.csv".format(LNA_no)
    csv_file=open(xx, mode='w')
    for i in range(0,len(NF)):
        xxx="{0},{1}\n".format(NF[i],Gain[i])
        #print(xxx)
        csv_file.write(xxx)
    csv_file.close()
