import instruments as ik
import sys,os
sys.path.insert(1, '/home/max/python/myimport')
import numpy as np
import SMU200
import N9000A
import time
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import SMF100

#########################################################33
#main program
####################################3
#TCP settings
#SMU200_host = '10.0.9.173'
N9000a_host='10.0.9.212'
SMF100_host = '10.0.9.197'

#variables
mydata=dict()
mydata["time"]={}
mydata["data"]={}
chck=dict()
f0=dict()
f2=dict()


#IF frequnecy
RF_freq=3050
RF_power=-35
LNA_no=1
BRO_no=17
time_nop=5
myoffset=0 #need to be specified
mod_choice=0
print("BRO NO ",BRO_no)
print("LNA NO ",LNA_no)
#



#initalization of instruments
N9000b=N9000A.N9000(N9000a_host)
#RF generator



#SMU200b=SMU200.SMU200(SMU200_host)
#SMU200b.single_freq(RF_power,RF_freq) #set iF
#SMU200b.RF_on()

#mcu1.set_LO_freq(LO_freq) #set LO_hmc836
SMF100b=SMF100.SMF100(SMF100_host)
SMF100b.single_freq(RF_power,RF_freq) #set RF
SMF100b.RF_on()





    #import matplotlib.pyplot as plt



N900_on='true'
#mydata=data()
mydata1=dict()
mydata1["acp"]={}
mydata1["ccdf"]={}
mydata1["spect"]={}
mydata1["spur"]={}
mydata1["sub_spur"]={}
mydata1["spur_mask"]={}
mydata1["obw"]={}
mydata1["chp"]={}

text="spur"+str(LNA_no)

#SMU200b.copy_picture1("")
#occupied bandwidth
#for LNA_no:range(1,4):

pdiv=10
ref=0
V_BW=3
R_bw=3
points=1000
S_freq=20
avg=1000
BW_limit=10


N9000b.OBwidth(pdiv,ref,V_BW,R_bw,avg,S_freq,RF_freq,points,BW_limit)
#time.sleep(6)
N9000b.set_title("OBW",text)
N9000b.set_XdB(-27)
N9000b.make_single_sweep()
mydata1["obw"]=list(N9000b.get_occ())
print("OCC BW",mydata1["obw"][0])
#print("XDB",mydata1["obw"][6])
#print("Frequnecy error",mydata1["obw"][5])
#print("CHannel power",mydata1["obw"][1])
#N9000b.N9000_data("pic2")
N9000b.copy_picture1("OBW{0}".format(LNA_no))

#spurious mask
pdiv=10
ref=0
V_bw=3
R_bw=3
S_freq=100 #*Rs #span frequnecy
points=1000
#S_freq=20
avg=2 #need to fiish measurement before request data
#set limits ?
offset=0
N9000b.Spurious_mask(pdiv,ref,V_bw,R_bw,avg,S_freq,RF_freq,points,myoffset)
#N9000b.make_single_sweep()
#time.sleep(2)
N9000b.set_title("SEMask",text)
N9000b.Spur_mask_limits(10)
N9000b.make_single_sweep()
mydata1["spur_mask"]["mask"]=list(N9000b.get_Spurious_mask())
mydata1["spur_mask"]["check"]=N9000b.check_Spurmask()
print(mydata1["spur_mask"]["check"])

#for i in range(len(mydata1["spur_mask"]["mask"])/7):
#    print("dB",mydata1["spur_mask"]["mask"][7*i+1])
#    print("Frequnecy",mydata1["spur_mask"]["mask"][7*i+4])
#N9000b.N9000_data("pic6")
file1="spur{0}".format(LNA_no)
print(file1+".png")
N9000b.copy_picture1(file1)
#input("")
import json
xx="LNA_{0}results.json".format(LNA_no)
with open(xx,'w') as file:
    json.dump(mydata1,file)
    #cPickle.dump(mydata.spect.freq,file)

file.close()





text="gr"
pdiv=10
ref=0
V_bw=.1
R_bw=.1
start_freq=1000
stop_freq=10000
points=5000
avg=4 #need to fiish measurement before request data
#set limits ?
#nomrailize power to 0dBm using the channel Power


myoffset=0
N9000b.Spurious_BRO(pdiv,ref,V_bw,R_bw,avg,stop_freq,start_freq,RF_freq,points,myoffset)
N9000b.copy_picture1("spur{0}_all".format(LNA_no))
N9000b.spur_subband_BRO(myoffset)
#N9000b.set_title("SPUR",text)

#N9000b.make_single_sweep()
mydata1["sub_spur"]=list(N9000b.get_spurious())
#for i in range(len(mydata1["sub_spur"])/6):
#    print("Spur no:",mydata1["sub_spur"][6*i+1])
#    print("Frequency [MHz]",mydata1["sub_spur"][6*i+3]/1e6)
#    print("Amplitude [dBm]",mydata1["sub_spur"][6*i+4])

N9000b.copy_picture1("spur{0}_zoom".format(LNA_no))
import json
filname="spurious_{0}.json".format(LNA_no)
with open(filname,'w') as file:
    json.dump(mydata1,file)
    #cPickle.dump(mydata.spect.freq,file)

file.close()


import os
#import mytest
from datetime import date
today = date.today()

i=0
while 1:
    if (os.path.isdir("RF{0}_LNA{1}_{2}".format(RF_freq,LNA_no,i)))!=1:
        os.system("mkdir RF{0}_LNA{1}_{2}".format(RF_freq,LNA_no,i))
        break
    i=i+1

if (os.path.isfile(file1+".png"))==1:
    os.system("mv *.png ./RF{0}_LNA{1}_{2}".format(RF_freq,LNA_no,i))
    #os.system("mv *.csv ./{0}_{1}".format(today,i))
    os.system("mv *.json ./RF{0}_LNA{1}_{2}".format(RF_freq,LNA_no,i))

i=0
os.system("mv ./RF{0}_LNA{1}_{2} ./../108340-{3}".format(RF_freq,LNA_no,i,BRO_no))
   
    
