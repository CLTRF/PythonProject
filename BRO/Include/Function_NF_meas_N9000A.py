#section 4.6 BIAS optimization
#from rssd.NRP_Common import PMr
#import visa
#import instruments as ik
import sys,os
#import instruments as ik

import csv
import copy
import logging
import time
from math import inf
from types import SimpleNamespace
import numpy as np
import gs_instrument
from gs_instrument import spectrum_analyzer
import numpy as np
#import SMU200
import time
import json
import datetime
import select
from gs_instrument import InstrumentDummy
from gs_instrument import CsvWriter

import time
import json
import numpy as np
# Bias optimization using
# -r&S power meter
# -SMU200A generator
# section bias optimization

#rm = visa.ResourceManager()

EXA=True

        #xx=self.N9000a.query("FETCH:FCAP?\n")
        #print(xx)
        #set up spand frequency to 10MHz

def NF_meas(self,start,stop,bw,avg,points):
    self.write("*RST\n")
    sa = "INST:NSEL 219\n"
    self.N9000a.write(sa)
    myfreq=2000
    points_command = ":SWE:POIN {0}\n"
    self.N9000a.write(points_command.format(points))
    sa = ":FREQ:STAR {0}{1}\n" #video BW
    self.N9000a.write(sa.format(start,"MHz"))
    sa = ":FREQ:STop {0}{1}\n" #resolution BW
    self.N9000a.write(sa.format(stop,"MHz"))
    sa = ":BANDWIDTH {0}{1}\n" #resolution BW
    self.N9000a.write(sa.format(bw,"MHz"))

    avg_command = ":AVER:COUN {0}\n"
    self.N9000a.write(avg_command.format(avg))
    self.N9000a.write(":AVER ON\n")
    self.N9000a.write(":INIT:CONT ON\n")

def NF_set_LO(self,mytype,lo):
    sa = ":MODE:{0}:LOSCillator:FREQuency {1}{2}\n"
    self.N9000a.write(sa.format(mytype,lo,"MHz"))
def recall_NFcal(self,myfil):
    self.N9000a.write(":MMEM:LOAD:STATE \"{0}\"\n".format(myfil))
    print(":MMEM:LOAD:STATE \"mytest.state \"\n")
def get_NF(self):
    points_query = ":FETCh:CORR:NFIG?"
    xx=self.N9000a.query(points_query)
    xx=self.N9000a.query(points_query)
    print(xx)
    if len(xx)>0:
        self.NF=[float(x) for x in xx.split(',')]
    points_query = ":FETCh:CORR:GAIN?"
    xx=self.N9000a.query(points_query)
    xx=self.N9000a.query(points_query)
    if len(xx)>0:
        self.Gain=[float(x) for x in xx.split(',')]
    return self.NF, self.Gain #return in MHz

"""
def Spurious_BRO(self,pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset): #spurious
    self.N9000a.write("*RST\n")
    sa = "INST:NSEL 1\n"
    self.N9000a.write(sa)
    sa = "INITiate:SPURious\n"
    self.N9000a.write(sa)

    self.N9000a.write(":INIT:CONT ON\n")
    #command for setting the center freq and span

    offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
    self.N9000a.write(offset_command.format(offset, "dB"))

    center_command = ":FREQ:CENTER {0:.2f} {1}\n"
    self.N9000a.write(center_command.format(C_freq, "MHz"))
    #points set up command
    sa1 = ":DISP:SPUR:VIEW:WIND:TRAC:Y:RLEV {0:.2f} dBm\n" #125" #reference level
    self.N9000a.write(sa1.format(ref))

    sa = ":DISP:SPUR:VIEW:WIND:TRAC:Y:PDIV {0:.2f} dB\n" #scale/div
        self.N9000a.write(sa.format(pdiv))

        points_command = ":SWE:POIN {0}\n"
        self.N9000a.write(points_command.format(points))

        sa = ":SPUR:FREQ:STAR {0}{1}\n" #video BW
        self.N9000a.write(sa.format(Start_freq,"MHz"))
        sa = "SPUR:FREQ:STop {0}{1}\n" #resolution BW
        self.N9000a.write(sa.format(Stop_freq,"MHz"))
        lim=-60
        sa = ":CALC:SPUR:LIM:ABS:DATA:STOP {:f}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format(lim))


        sa = ":SPUR:STAT {0}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format("on"))


        #sa = "SPUR:BAND:VID {0} {1}" #video BW
        #self.N9000a.write(sa.format(V_bw,"MHz"))
        #sa = "SPUR:BAND {0:.2f} {1}" #resolution BW
        #self.N9000a.write(sa.format(R_bw,"MHz"))

        avg_command = "SPUR:AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write("SPUR:AVER ON\n")
        self.make_single_sweep()



        #self.N9000a.write(":INIT:CONT OFF\n")
        #self.N9000a.write("*WAI\n")
        #self.N9000a.write(":INIT:IMM\n")
    def spur_subband_BRO(self,offset):
        lim=-50
        self.N9000a.write(":INIT:CONT ON\n")
        offset_command = "DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))
        sa = "CALC:SPUR:LIM:ABS:DATA:STOP {:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format(lim,lim,lim,lim,lim,lim,lim,lim,lim,lim))

        sa = ":SPUR:STAT {0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format("on","on","on","on","on","on","on","on","on","on"))
        sa = "SPUR:FREQ:STAR {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        self.N9000a.write(sa.format(1000,3000,3900,4900,5900,6900,10800,15400,17500,18200))
        sa = "SPUR:FREQ:STop {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        self.N9000a.write(sa.format(3000,3900,4900,5900,6900,10800,15400,17500,18200,26000))
        points=1001
        sa = "SPUR:SWE:POIN {0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n" #video BW
        self.N9000a.write(sa.format(points,points,points,points,points,points,points,points,points,points))

        RES_BW=100000
        #RES_BW1=10000
        sa = "SPUR:band {0}Hz,{1}Hz,{2}Hz,{3}Hz,{4}Hz,{5}Hz,{6}Hz,{7}Hz,{8}Hz,{9}Hz\n" #video BW
        self.N9000a.write(sa.format(RES_BW,RES_BW,RES_BW,RES_BW,RES_BW,RES_BW,RES_BW,RES_BW,RES_BW,RES_BW))
        #self.N9000a.write("*WAI\n")
        self.N9000a.write("SPUR:SPUR 1\n") #dirty code




#########################################################33
#main program
####################################3

#V_BW
#R_BW

mm='xx'
if mm=="true":
    #import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.pyplot as plt


    N9000a_host='10.0.8.51'
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



    N9000b=N9000(N9000a_host)
    xx=N9000b.get_points()

    #occupied bandwidth
    #spectrum
    S_freq=100
    C_freq=1200
    ref=0
    pdiv=10
    points=1001
    avg=1000
    N9000b.Spectrum(pdiv,ref,0,0,avg,S_freq,C_freq,points)
    N9000b.make_single_sweep()
    #time.sleep(2)
    N9000b.save_spectrum("pic1",1,S_freq,C_freq,points)
    N9000b.copy_picture1("pic1")


    #occupied bandwidth
    pdiv=10
    ref=0
    V_BW=3
    R_bw=3
    C_freq=1200
    points=1000
    S_freq=20
    avg=1000
    BW_limit=5

    N9000b.OBwidth(pdiv,ref,V_BW,R_bw,avg,S_freq,C_freq,points,BW_limit)
    #time.sleep(6)
    N9000b.set_XdB(-27)
    N9000b.make_single_sweep()
    mydata1["obw"]=list(N9000b.get_occ())
    print("OCC BW",mydata1["obw"][0])
    print("XDB",mydata1["obw"][6])
    print("Frequnecy error",mydata1["obw"][5])
    print("CHannel power",mydata1["obw"][1])


    N9000b.N9000_data("pic2")
    N9000b.copy_picture1("pic2")

    #Adjecent channel power
    pdiv=10
    ref=0
    V_bw=0
    R_bw=0
    C_freq=1200
    points=1000
    S_freq=10
    avg=200
    acp_limit=-20 #relative to the carrier in dB
    N9000b.ACPower(pdiv,ref,V_bw,R_bw,avg,S_freq,C_freq,points,acp_limit)
    N9000b.make_single_sweep()
    mydata1["acp"]=list(N9000b.get_ACP())
    print("Reference ACP",mydata1["acp"][0])
    print("Lower ACP [dBc]",mydata1["acp"][1])
    print("Upper ACP [dBc]",mydata1["acp"][2])
    N9000b.N9000_data("pic3")
    N9000b.copy_picture1("pic3")


    #input("Press Enter to continue...")
    #channel power
    pdiv=5
    ref=0
    V_bw=0
    R_bw=0
    avg=200
    C_freq=1200
    points=1000
    S_freq=1


    N9000b.CHpower(pdiv,ref,V_bw,R_bw,avg,S_freq,C_freq,points)
    N9000b.make_single_sweep()
    #time.sleep(2)
    mydata1["chp"]=list(N9000b.get_CHpower())
    print("Channel power [dBm]",mydata1["chp"][0])
    print("Power Spectral Densisty [dBm/Hz]",mydata1["chp"][1])
    N9000b.N9000_data("pic4")
    N9000b.copy_picture1("pic4")


    #spurious
    pdiv=10
    ref=0
    V_bw=3
    R_bw=3
    C_freq=5200
    start_freq=1000
    stop_freq=10000
    points=1000
    avg=5 #need to fiish measurement before request data
    #set limits ?
    #nomrailize power to 0dBm using the channel Power


    #points?
    N9000b.Spurious(pdiv,ref,V_bw,R_bw,avg,stop_freq,start_freq,C_freq,points,0)

    N9000b.make_single_sweep()
    mydata1["spur"]=list(N9000b.get_spurious())
    for i in range(len(mydata1["spur"])/6):
        print("Spur no:",mydata1["spur"][6*i+1])
        print("Frequency [MHz]",mydata1["spur"][6*i+3]/1e6)
        print("Amplitude [dBm]",mydata1["spur"][6*i+4])
    N9000b.N9000_data("pic5")
    N9000b.copy_picture1("pic5")
    offset=-1*mydata1["spur"][4]
    N9000b.check_spur_subband(offset)
    mydata1["sub_spur"]=list(N9000b.get_spurious())
    for i in range(len(mydata1["sub_spur"])/6):
        print("Spur no:",mydata1["sub_spur"][6*i+1])
        print("Frequency [MHz]",mydata1["sub_spur"][6*i+3]/1e6)
        print("Amplitude [dBm]",mydata1["sub_spur"][6*i+4])


    #spurious mask
    pdiv=5
    ref=0
    V_bw=3
    R_bw=3
    C_freq=1200 #center frequency
    S_freq=1000 #span frequnecy
    points=1000
    #S_freq=20
    avg=5 #need to fiish measurement before request data
    #set limits ?

    N9000b.Spurious_mask(pdiv,ref,V_bw,R_bw,avg,S_freq,C_freq,points)
    #N9000b.make_single_sweep()
    #time.sleep(2)
    N9000b.make_single_sweep()
    mydata1["spur_mask"]["mask"]=list(N9000b.get_Spurious_mask())
    mydata1["spur_mask"]["check"]=N9000b.check_Spurmask()
    print(mydata1["spur_mask"]["check"])

    for i in range(len(mydata1["spur_mask"]["mask"])/7):
        print("dB",mydata1["spur_mask"]["mask"][7*i+1])
        print("Frequnecy",mydata1["spur_mask"]["mask"][7*i+4])
    N9000b.N9000_data("pic6")
    N9000b.copy_picture1("pic6")
    #input("")

    #make CCDF
    C_freq=1200 #MHz center freq
    info_bw=10 #10mHz info bandwidth
    N9000b.CCDF(info_bw,C_freq)
    import time
    time.sleep(10)
    mydata1["ccdf"]=N9000b.get_CCDF()
    print("Channel Power",mydata1["ccdf"][0])
    print("",mydata1["ccdf"][1],"% at 0dB")
    print("10%",mydata1["ccdf"][2],"dB")
    print("1%",mydata1["ccdf"][3],"dB")
    print("0.1%",mydata1["ccdf"][4],"dB")
    print("0.01%",mydata1["ccdf"][5],"dB")
    print("0.001%",mydata1["ccdf"][6],"dB")
    print("0.0001%",mydata1["ccdf"][7],"dB")
    print("Peak",(mydata1["ccdf"][8]),"dB")
    N9000b.N9000_data("pic7")
    N9000b.copy_picture1("pic7")


    import json
    with open('hello.txt','w') as file:
        json.dump(mydata1,file)
        #cPickle.dump(mydata.spect.freq,file)

    file.close()


    #time.sleep(10)
    #input("")


    import mygen2

    print("make pdf file")
    import mytest
    os.system('cp full.pdf ~max/share')
    import os
    #import mytest
    from datetime import date
    today = date.today()

    i=0
    while 1:
        if (os.path.isdir("{0}_{1}".format(today,i)))!=1:
            os.system("mkdir {0}_{1}".format(today,i))
            break
        i=i+1

    if (os.path.isfile("pic1.png"))==1:
        os.system("mv *.png ./{0}_{1}".format(today,i))
        os.system("mv *.csv ./{0}_{1}".format(today,i))
    print(os.path.isfile("full.*"))
    if (os.path.isfile("full.tex"))==1:
        os.system("mv full*.* ./{0}_{1}".format(today,i))

"""