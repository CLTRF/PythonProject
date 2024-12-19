#section 4.6 BIAS optimization
#from rssd.NRP_Common import PMr
#import visa
#import instruments as ik
import sys,os
import instruments as ik

import time
import json
import numpy as np
# Bias optimization using
# -r&S power meter
# -SMU200A generator
# section bias optimization

#rm = visa.ResourceManager()

EXA=True




class N9000:
# call N9000.get_points()
    def __init__(self,N9000ahost,picture=False):
        self.N9000a= ik.generic_scpi.SCPIInstrument.open_tcpip(N9000ahost, 5025)
        if picture==False:
            info= self.N9000a.query("*IDN?")
            print("Info:"+ str(info))
            self.N9000a.write("*RST\n")


    def set_XdB(self,myxdB):
        xdb_command = "OBW:XDB {0:.2f} {1}\n"
        self.N9000a.write(xdb_command.format(myxdB, "dB"))


    def get_points(self):
        #get points
        points_query = ":SWE:POIN?"
        points= self.N9000a.query(points_query)
        print("points",points)
        return points


    def get_ACP(self):
        points_query = ":FETCh:ACPower?"
        xx=self.N9000a.query(points_query)
        points_query = "CALC:CLIM:FAIL?\n"
        yy=float(self.N9000a.query(points_query))
        if yy<1:
            print("OCC pass")
        else:
            print("OCC fail")
        if len(xx)>0:
            self.acp=[float(x) for x in xx.split(',')]
        self.acp.append(yy)
        print("OCC",self.acp)
        return self.acp #return in MHz

    def get_CHpower(self):
        points_query = ":FETCh:CHPower?"
        xx=self.N9000a.query(points_query)
        if len(xx)>0:
            self.chpower = [float(x) for x in xx.split(',')]
        return self.chpower #return in MHz

    def get_spurious(self):
        points_query = ":FETCh:SPURious?"
        xx=self.N9000a.query(points_query)
        if len(xx)>0:
            self.spur = [float(x) for x in xx.split(',')]
        return self.spur #return in MHz


    def get_Spurious_mask(self):
        points_query = ":FETCh:SEMask?"
        xx=self.N9000a.query(points_query)
        points_query = ":FETCh:SEMask?"
        xx=self.N9000a.query(points_query)
        if len(xx)>0:
            self.mask = [float(x) for x in xx.split(',')]
        return self.mask #return in MHz

    def check_Spurmask(self):
        points_query = "CALC:CLIM:FAIL?\n"
        xx=self.N9000a.query(points_query)
        if xx==1:
            xx="FAIL"
        else:
            xx="PASS"
        return xx #return in MHz


    def get_CCDF(self):
        points_query = ":FETCh:PSTatistic?"
        xx=self.N9000a.query(points_query)
        points_query = ":FETCh:PSTatistic?"
        xx=self.N9000a.query(points_query)
        if len(xx)>0:
            self.ccdf=[float(x) for x in xx.split(',')]
        return self.ccdf #return in MHz

    def get_occ(self):
        points_query = ":FETCh:OBWidth?\n"
        xx= (self.N9000a.query(points_query))
        points_query = "CALC:CLIM:FAIL?\n"
        yy=float(self.N9000a.query(points_query))
        if yy==0.0:
            print("OCC pass")
        else:
            print("OCC fail")
        if len(xx)>0:
            self.Occ=[float(x) for x in xx.split(',')]
        self.Occ.append(yy)
        #print("OCC",self.Occ)
        self.N9000a.write(":INIT:CONT ON\n")
        return self.Occ #return in MHz
    #def get_phnoise(self):
    def get_phnoise(self,filname):
        time.sleep(2)

        xx1=":MMEM:STOR:results:MTABle \"C:\Temp\{0}.csv\"\n"
        #print("fil:",xx1.format(filname))
        self.N9000a.write(xx1.format(filname))

        self.N9000a.write("*OPC\n")

        xx2="MMEM:DATA? \"C:\Temp\{0}.csv\"\n"
        self.N9000a.write(xx2.format(filname))
        capture = self.N9000a.binblockread(1) #":MMEM:DATA? \"c:\Temp\pic1.png\"\n")#, datatype='c',is_big_endian=True) #,container=list)#,

        with open('{0}.csv'.format(filname), 'wb') as f:
            f.write(capture)
        f.close()
        self.N9000a.query("*CLS\n")
        self.N9000a.write(":MMEM:DEL \"C:\Temp\{0}.csv\"\n".format(filname))



    def phase_noise(self,no):
        #set marker mode norma

        if no==2:
            offset=10000. #Hz
            xx=2
        elif no==1:
            offset=1. #Hz
            xx=4
        else:
            offset=1. #Hz
            xx=6

        for i in range(0,xx):
            offset=offset*10 #Hz
            mark=2+i
            marker_on = "CALC:MARK{:d}:STAT ON\n"
            self.N9000a.write(marker_on.format(mark))
            marker_on = "CALC:MARK{:d}:MODE DELT\n"
            self.N9000a.write(marker_on.format(mark))

            marker_on = "CALC:MARK{:d}:REF 1\n"
            self.N9000a.write(marker_on.format(mark))

            marker_on = "CALC:MARK{:d}:FUNC BDEN\n"
            self.N9000a.write(marker_on.format(mark))
            marker_on = ":CALC:MARK{:d}:FUNC:BAND:SPAN 1 Hz\n"
            self.N9000a.write(marker_on.format(mark))
            marker_on = ":CALC:MARK{:d}:X {:.6f} MHZ\n"
            self.N9000a.write(marker_on.format(mark,offset/1e6))

        marker_on = "CALC:MARK:TABL ON\n"
        self.N9000a.write(marker_on)

    def set_title(self,meastype,mytitle):
        #meas type is OBW,CHP,ACP,SPUR,SEMask
        if meastype=="SAN":
            self.N9000a.write("DISP:ANN:TITL:DATA \"{0}\" \n".format(mytitle))
        else:
            self.N9000a.write("DISP:{0}:ANN:TITL:DATA \"{1}\" \n".format(meastype,mytitle))

    def noise_marker(self,marker,myfreq,myresbw):
        marker_on = ":CALC:MARK{:d}:STAT ON\n"
        self.N9000a.write(marker_on.format(marker))
        self.N9000a.write(":CALC:MARK{:d}:X {:.3f}MHz\n".format(marker,float(myfreq)))
        self.N9000a.write("CALC:MARK{:d}:FUNC NOIS\n".format(marker))

        self.N9000a.write(":CALC:MARK{:d}:FUNC:BAND:SPAN {:f} MHz\n".format(marker,float(myresbw)))
        marker_on = ":CALC:MARK{:d}:X?\n"
        xx=self.N9000a.query(marker_on.format(marker))
        marker_on = ":CALC:MARK{:d}:Y?\n"
        yy=self.N9000a.query(marker_on.format(marker))
        zz=self.N9000a.query(":band?\n")

        #print(xx,yy)
        return [float(xx),float(yy),float(zz)]

    def get_marker(self,marker):
        marker_on = ":CALC:MARK{:d}:X?\n"
        xx=self.N9000a.query(marker_on.format(marker))
        marker_on = ":CALC:MARK{:d}:Y?\n"
        yy=self.N9000a.query(marker_on.format(marker))
        #print(xx,yy)
        return [float(xx),float(yy)]
    def get_band_marker(self,marker,myfreq,bw_res):
        marker_on = ":CALC:MARK{:d}:STAT ON\n"
        self.N9000a.write(marker_on.format(marker))
        self.N9000a.write(":CALC:MARK{:d}:X {:.3f}MHz\n".format(marker,float(myfreq)))
        self.N9000a.write("CALC:MARK{:d}:FUNC BPOW\n".format(marker))

        self.N9000a.write(":CALC:MARK{:d}:FUNC:BAND:SPAN {:f} MHz\n".format(marker,float(bw_res)))
        marker_on = ":CALC:MARK{:d}:X?\n"
        xx=self.N9000a.query(marker_on.format(marker))
        time.sleep(1)
        marker_on = ":CALC:MARK{:d}:Y?\n"
        yy=self.N9000a.query(marker_on.format(marker))
        zz=self.N9000a.query(":band?\n")
        return [float(xx),float(yy),float(zz)]

    def Markerpeak(self, marker):
        #set marker mode normal
        marker_on = ":CALC:MARK{:d}:STAT ON\n"
        self.N9000a.write(marker_on.format(marker))
        #marker_on = ":CALC:MARK{:d}:MODE POS\n"

        #self.N9000a.write(marker_on.format(marker))
        time.sleep(1)
        marker_on = ":CALC:MARK{:d}:MAX\n"
        #set marker at modulation freq
        self.N9000a.write(marker_on.format(marker))
        #self.markers[marker-1] = True

    def marker_refl(self, marker):
        #set marker mode normal
        ref_level_command = ":DISP:WIND:TRACE:Y:RLEVEL 0 dBm\n"
        self.N9000a.write(ref_level_command)
        marker_on = "CALC:MARK{0}:RLEV\n"
        #set marker at modulation freq
        self.N9000a.write(marker_on.format(marker))
        #self.markers[marker-1] = True
    def markers_off(self,marker):
        if marker=="all":
            for i in range(1,12):
                marker_off = ":CALC:MARK{:d}:STAT OFF\n"
                self.N9000a.write(marker_off.format(i))


    def marker_cef(self, marker):
        #set marker mode normal
        marker_on = "CALC:MARK{0}:CENT\n"
        #set marker at modulation freq
        self.N9000a.write(marker_on.format(marker))
        #self.markers[marker-1] = True
    def set_marker(self, marker,myfreq):
        #set marker mode normal
        self.N9000a.write(":CALC:MARK{:d}:X {:.3f}MHz\n".format(marker,float(myfreq)))
        #set marker at modulation freq
        #self.N9000a.write(marker_on.format(marker,freq))
        #self.markers[marker-1] = True
    def table_markers(self,on_off=False):
        #set marker mode normal
        if on_off==True:
            self.N9000a.write("CALC:MARK:TABL ON\n")
        else:
            self.N9000a.write("CALC:MARK:TABL OFF\n")
        #set marker at modulation freq
        #self.N9000a.write(marker_on.format(marker,freq))
        #self.markers[marker-1] = True
    def set_attuation(self,dB_value):
        #set marker mode normal
        self.N9000a.write("pow:ATT {0:.2f}\n".format(float(dB_value)))
        #set marker at modulation freq
        #self.N9000a.write(marker_on.format(marker,freq))
        #self.markers[marker-1] = True

    def Spectrum(self,scale,ref_level,V_BW,R_BW,avg,span_freq,cen_freq,points,f_offset=0,dB_offset=0,maxhold=True):
        #command for setting the mode as the Spectrum Analyser
        if scale=="auto":
            self.N9000a.write("*RST\n")
            sa = "INST:NSEL 1\n"
            self.N9000a.write(sa)
            #format trace in ascii:
            self.N9000a.write(":FREQ:TUNE:IMM\n")

        else:
            self.N9000a.write("*RST\n")
            sa = "INST:NSEL 1\n"
            self.N9000a.write(sa)
            #format trace in ascii:
            self.N9000a.write(":INIT:CONT ON\n")
            #command for span with format
            center_command = "FREQ:offset {0:.8f} {1}\n"
            self.N9000a.write(center_command.format(f_offset, "Hz"))

            offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
            self.N9000a.write(offset_command.format(dB_offset, "dB"))

            span_command = "FREQ:SPAN {0:.8f} {1}\n"
            #command for setting the center freq
            center_command = "FREQ:CENTER {0:.8f} {1}\n"
            self.N9000a.write(span_command.format(span_freq, "MHz"))
            self.N9000a.write(center_command.format(cen_freq, "MHz"))


            if R_BW>0:
                rbw_command = "BAND {0} MHZ\n"
                self.N9000a.write(rbw_command.format(R_BW, "MHz"))
            #command for setting ref level:
            ref_level_command = ":DISP:WIND:TRACE:Y:RLEVEL {0:.2f} dBm\n"
            #command for setting the scale per div
            scale_command = ":DISP:WIND:TRACE:Y:PDIV {0:.2f} dB\n"
            self.N9000a.write(ref_level_command.format(ref_level))
            self.N9000a.write(scale_command.format(scale))
            #points set up command
            points_command = ":SWE:POIN {0}\n"
            self.N9000a.write(points_command.format(points))
            #continues mode
            avg_command = "AVER:COUN {0}\n"
            self.N9000a.write(avg_command.format(avg))

            if maxhold==True:
                self.N9000a.write("TRAC1:TYPE MAXH\n") #set maxhold on trace 1
            if maxhold=="avg":
                self.N9000a.write("TRAC1:TYPE AVER\n") #set maxhold on trace 1
            #print(self.N9000a.query("SENS:SWE:TIME?\n")) #time of a speed
            #self.N9000a.write(":INIT:CONT OFF\n")
            #self.N9000a.write("INIT:IMM\n")

            #time.sleep(2)
            #info=self.N9000a.query("*OPC?\n")
            #info= self.N9000a.query("*IDN?")
            #print("Info:"+ str(info))
    def OBwidth(self,p_div,ref_level,V_BW,res_bw,avg,span_freq,cen_freq,points,bw_limit,dB_offset=0):
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 1\n"
        self.N9000a.write(sa)
        sa = "INITiate:OBWidth\n"
        self.N9000a.write(sa)
        #print(dB_offset)
        offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(dB_offset, "dB"))
        sa = "DISP:OBW:VIEW:WIND:TRAC:Y:RLEV {0:0.2f} dBm\n"#125" #reference level
        self.N9000a.write(sa.format(ref_level))
        sa = "DISP:OBW:VIEW:WIND:TRAC:Y:PDIV {0:.2f} dB\n" #scale/div
        self.N9000a.write(sa.format(p_div))
        sa = "DISP:OBW:VIEW:WIND:TRAC:Y:RPOS TOP\n" #ref pos
        self.N9000a.write(sa)
        sa = "OBW:BAND:VID {0} {1}\n" #video BW
        self.N9000a.write(sa.format(V_BW,"MHz"))
        sa = "OBW:BAND {0:.2f} {1}\n" #resolution BW
        self.N9000a.write(sa.format(res_bw,"MHz"))
                #format trace in ascii:
        BW_lim = ":CALC:OBW:LIMit:FBLimit {0} {1}\n"
        self.N9000a.write(BW_lim.format(bw_limit,"MHz")) #set limits
        self.N9000a.write(":CALC:OBW:LIM ON\n") #set limits on
        #command for span with format
        span_command = ":OBW:FREQ:SPAN {0} {1}\n"
        #command for setting the center freq
        center_command = "FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(span_command.format(span_freq, "MHz"))
        self.N9000a.write(center_command.format(cen_freq, "MHz"))
        #points set up command
        points_command = ":SWEEP:POINTS {0}\n"
        self.N9000a.write(points_command.format(points))

        avg_command = "OBW:AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write("OBW:AVER ON\n")
        self.N9000a.write("TRAC:OBW:TYPE MAXH\n")#max hold
        #self.N9000a.write("*WAI\n")
        #self.N9000a.write("*RST\n")
        #set x vlaue typical -27dB
        #get occ bandwidth
        #ind=self.N9000a.query_ascii_values(":FETCh:OBWidth:XDB?")
        #print("hello",ind[1])
        #get x dB bandwidth
        self.N9000a.write(":INIT:CONT ON\n")

    def CHpower(self,pdiv,ref_level,V_bw,int_bw,avg,S_freq,C_freq,points,dB_offset=0,bw=5): #channel power
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 1\n"
        self.N9000a.write(sa)
        sa = "INITiate:CHPower\n"
        self.N9000a.write(sa)
        self.N9000a.write(":INIT:CONT ON\n")
        #print bw
        self.N9000a.write(":CHP:BAND:INT {0} MHz\n".format(bw))
        #sa = "CHPower:BAND:VID {0} {1}\n" #video BW
        #self.N9000a.write(sa.format(V_bw,"MHz"))
        #sa = "CHPower:BAND {0:.2f} {1}" #resolution BW
        #self.N9000a.write(sa.format(R_bw,"MHz"))
        offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(dB_offset, "dB"))
        span_command = ":CHPower:FREQ:SPAN {0} {1}\n" #setting the frequency span
        center_command = "FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(C_freq, "MHz"))
        self.N9000a.write(span_command.format(2*S_freq, "MHz"))
        sa = "DISP:CHPower:VIEW:WIND:TRAC:Y:RLEV {0:0.2f} dBm\n"#125" #reference level
        self.N9000a.write(sa.format(ref_level))

        #points set up command
        points_command = ":SWE:POIN {0}\n"
        self.N9000a.write(points_command.format(points))
        self.N9000a.write("CHP:BAND:AUTO ON\n")
        #self.N9000a.write("CHP:VID:AUTO ON\n")
        #self.N9000a.write("CHP:BAND:INT {}MHz\n".format(int_bw))
        self.N9000a.write(":CHP:BAND:INT {0} MHz\n".format(bw))
        self.N9000a.write("TRAC:CHP:TYPE AVER\n")#max hold
        avg_command = "CHP:AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write(":INIT:CONT ON\n")


    def ACPower(self,pdiv,ref,V_bw,R_bw,avg,S_freq,C_freq,points,acp_lim,dB_offset=0,Rs=3): #channel power
        self.N9000a.write("*RST\n")
        self.N9000a.write("INST:NSEL 1\n")
        self.N9000a.write("INITiate:ACPower\n")
        self.N9000a.write(":INIT:CONT ON\n")
        span_command = ":ACPower:FREQ:SPAN {0} {1}\n"
        offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(dB_offset, "dB"))
        sa = "DISP:ACPower:VIEW:WIND:TRAC:Y:RLEV {0:0.2f} dBm\n"#125" #reference level
        self.N9000a.write(sa.format(ref))
        #command for setting the center freq and span
        center_command = "FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(span_command.format(S_freq, "MHz"))
        self.N9000a.write(center_command.format(C_freq, "MHz"))
        #points set up command
        points_command = ":SWE:POIN {0}\n"
        self.N9000a.write(points_command.format(points))
        acplimits = "ACP:OFFS:LIST:RCAR {0},{1},0,0,0,0\n"
        self.N9000a.write(acplimits.format(acp_lim,acp_lim))

        self.N9000a.write("CALC:ACP:LIM:STAT ON\n") #set limits on
        #bw_cmd="CHP:BAND {0} MHz\n"
        #self.N9000a.write(bw_cmd.format(R_bw))
        #bw_cmd="CHP:BAND:VID {0} MHz\n"
        #self.N9000a.write(bw_cmd.format(V_bw))

        self.N9000a.write("ACP:BAND:AUTO ON\n")
        #self.N9000a.write("ACP:BAND:VID:AUTO ON\n")

        f_offset=0.5*Rs
        #limits
        #set offset frequnecy
        self.N9000a.write("ACP:OFFS:LIST {0} MHz,0,0,0,0,0\n".format(f_offset)) #

        #set offset frequnecy bandwidth
        sa="ACP:OFFS:LIST:BAND {0}MHz,0,0,0,0,0\n".format(0.2*Rs)
        self.N9000a.write(sa)
        #set center noise bandwidth
        sa="ACP:CARR1:LIST:BAND {0}MHz\n".format(0.2*Rs)
        self.N9000a.write(sa)

        self.N9000a.write("TRAC:ACP:TYPE MAXH\n")#max hold
        avg_command = "ACP:AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write(":INIT:CONT ON\n")


    def Spurious(self,pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset): #spurious
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 1\n"
        self.N9000a.write(sa)
        sa = "INITiate:SPURious\n"
        self.N9000a.write(sa)

        self.N9000a.write(":INIT:CONT ON\n")
        #command for setting the center freq and span
        self.N9000a.write(":DISP:SPUR:VIEW:WIND:TRAC:Y:COUP OFF\n")
        offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))

        center_command = ":FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(C_freq, "MHz"))
        #points set up command
        sa1 = ":DISP:SPUR:VIEW:WIND:TRAC:Y:RLEV {0:.2f} dBm\n" #125" #reference level
        self.N9000a.write(sa1.format(ref))
        sa = ":DISP:SPUR:VIEW:WIND:TRAC:Y:PDIV {0:.2f}\n" #scale/div
        self.N9000a.write(sa.format(pdiv))


        #sa = ":DISP:SPUR:VIEW:WIND:TRAC:Y:PDIV {0:.2f}\n" #scale/div
        #self.N9000a.write(sa.format(pdiv))

        points_command = ":SWE:POIN {0}\n"
        self.N9000a.write(points_command.format(points))

        sa = ":SPUR:FREQ:STAR {0}{1}\n" #video BW
        self.N9000a.write(sa.format(Start_freq,"MHz"))
        sa = "SPUR:FREQ:STop {0}{1}\n" #resolution BW
        self.N9000a.write(sa.format(Stop_freq,"MHz"))
        #self.N9000a.write(":INIT:CONT ON\n")

        #self.N9000a.write(":CALC:MARK{:d}:STAT ON\n")
        #self.N9000a.write(":CALC:SPUR:MARK1:MAX\n")
        #yy=float(self.N9000a.query(":CALC:SPUR:MARK1:Y?"))
        #print yy
        #if offset==1:
        #    offset_command = ":DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        #    self.N9000a.write(offset_command.format(-1*yy, "dB"))


        lim=-60.0

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


        self.N9000a.write(":INIT:CONT ON\n")


        #self.N9000a.write(":INIT:CONT OFF\n")
        #self.N9000a.write("*WAI\n")
        #self.N9000a.write(":INIT:IMM\n")
    def check_spur_subband(self,offset):
        lim=-60
        self.N9000a.write(":INIT:CONT ON\n")
        offset_command = "DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))
        sa = "CALC:SPUR:LIM:ABS:DATA:STOP {:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format(lim,lim,lim,lim,lim,lim,lim,lim,lim,lim))

        sa = ":SPUR:STAT {0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format("on","on","on","on","on","on","on","on","on","on"))
        sa = "SPUR:FREQ:STAR {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        self.N9000a.write(sa.format(500,2000,3000,4000,5000,6000,7000,8500,9000,500))
        sa = "SPUR:FREQ:STop {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        self.N9000a.write(sa.format(1000,3000,4000,5000,6000,7000,8000,9000,10000,10000))

        self.N9000a.write(":SPUR:RANGE:10\n")

    def check_spur_subband1(self,C_freq,offset):
        lim=-60
        self.N9000a.write(":INIT:CONT ON\n")
        offset_command = "DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))
        sa = "CALC:SPUR:LIM:ABS:DATA:STOP {:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        self.N9000a.write(sa.format(lim,lim,lim,lim,lim,lim,lim,lim,lim,lim))

        sa = ":SPUR:STAT {0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n"#{2} {3} {4} {5} {6} {7} {8}\n" #video BW
        x_on=["on","on","on","on","on","on","on","on","on","on"]
        self.N9000a.write(sa.format(x_on[0],x_on[1],x_on[2],x_on[3],x_on[4],x_on[5],x_on[6],x_on[7],x_on[8],x_on[9]))

        sa = "SPUR:FREQ:STAR {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        f_start=[C_freq-1000,C_freq-400.0,C_freq-300.0,C_freq-200.0,C_freq+50.0,C_freq+200.0,C_freq+300.0,C_freq+400.0,C_freq+500.0,7000]
        f_stop=[C_freq-400,C_freq-300.0,C_freq-200.0,C_freq-50.0,C_freq+200.0,C_freq+300.0,C_freq+400.0,C_freq+500.0,C_freq+1000.0,9000]
        #print(f_start)
        self.N9000a.write(sa.format(f_start[0],f_start[1],f_start[2],f_start[3],f_start[4],f_start[5],f_start[6],f_start[7],f_start[8],f_start[9]))
        sa = "SPUR:FREQ:STop {0}MHz,{1}MHz,{2}MHz,{3}MHz,{4}MHz,{5}MHz,{6}MHz,{7}MHz,{8}MHz,{9}MHz\n" #video BW
        self.N9000a.write(sa.format(f_stop[0],f_stop[1],f_stop[2],f_stop[3],f_stop[4],f_stop[5],f_stop[6],f_stop[7],f_stop[8],f_stop[9]))


        #self.N9000a.write(":SPUR:RANGE:10\n")



    def Spurious_mask(self,pdiv,ref,V_bw,R_bw,avg,S_freq,C_freq,points,offset): #spurious
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 1\n"
        self.N9000a.write(sa)
        sa = "INITiate:SEMask\n"
        self.N9000a.write(sa)

        offset_command = "DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))
        span_command = "DISP:SEM:VIEW:WIND:TRAC:X:PDIV {0} {1}\n"
        #command for setting the center freq and span
        center_command = "FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(C_freq, "MHz\n"))
        self.N9000a.write(span_command.format(S_freq/10,"MHz\n"))
        points_command = ":INIT:CONT ON\n"
        self.N9000a.write(points_command.format(points)) #continues sweep

        sa = "DISP:SEMask:VIEW:WIND:TRAC:Y:RLEV {0:0.2f} dBm\n"#125" #reference level
        self.N9000a.write(sa.format(ref))
        sa = "DISP:SEMask:VIEW:WIND:TRAC:Y:PDIV {0:.2f} dB\n" #scale/div
        self.N9000a.write(sa.format(pdiv))
        avg_command = "SEMask:AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write("SEMask:AVER ON\n")
        self.N9000a.write("SEM:TYPE SPREF\n") #realative amplitude settings

        #points_command = ":INIT:CONT OFF\n" #single sweep


            #start frequnecy semask:offset1:list:frequenc:start 120mHz
            #stop frequnecy
            #amplitude
    def Spur_mask_limits(self,bitrate,resBW="auto"):
        #usinf ECSS recommendations
        #0.5Rs 0 dB
        #1.4Rs -30dB
        #3Rs -60dB
        Rs=bitrate #symbol bitrate in MHz
        self.N9000a.write("SEMask:OFFSET1:LIST:FREQuency:STARt {:.2f}MHz,{:.2f}MHz,{:.2f}MHz,{:.2f}MHz\n".format(Rs/10.0,0.5*Rs,1.4*Rs,3.*Rs))
        self.N9000a.write("SEMask:OFFSET1:LIST:FREQuency:STOP {:.2f}MHz,{:.2f}MHz,{:.2f}MHz,{:.2f}MHz\n".format(0.5*Rs,1.4*Rs,3.*Rs,5.*Rs))
        self.N9000a.write("SEM:OFFS:LIST:STAT ON, ON, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF\n") #on off
        self.N9000a.write("SEM:OFFS:LIST:STAR:RCAR 0,0,-30,-60\n") #realative amplitude start settings
        self.N9000a.write("SEM:OFFS:LIST:STOP:RCAR 0,-30,-60,-60\n") #realative amplitude stop settings
        self.N9000a.write("SEM:OFFS:LIST:TEST REL, REL, REL,REL\n") #realative amplitude stop settings
        self.N9000a.write("SEM:OFFS:LIST:BAND:AUTO 1,1,1,1\n") #realative amplitude stop settings
        if resBW=="auto":
            print("1")
        else:
            self.N9000a.write("SEM:OFFS2:LIST:BAND {:.2f}kHz,{:.2f}kHz,{:.2f}kHz,{:.2f}kHz\n".format(1.0*resBW,1.0*resBW,1.0*resBW,1.0*resBW)) #realative amplitude stop settings
        self.N9000a.write("SEM:OFFS2:LIST:BAND:VID:AUTO ON,ON,ON,ON\n") #realative amplitude stop settings
        xx1=(self.N9000a.query("SEM:OFFS2:LIST:BAND?\n"))
        if len(xx1)>0:
            xx = [float(x) for x in xx1.split(',')]

        #print(xx)
        self.N9000a.write("SEM:OFFS:LIST:BAND {:f},{:f},{:f},{:f}\n".format(xx[0],xx[1],xx[2],xx[1])) #re
        xx=self.N9000a.query("SEM:OFFS2:LIST:BAND?\n")
        #print(xx)
        self.N9000a.write("DISP:SEM:VIEW RPFR\n")


    def CCDF(self,info_bw,C_freq,offset): #CCDF
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 1\n"
        self.N9000a.write(sa)
        sa = "INITiate:PSTatistic\n"
        self.N9000a.write(sa)
        center_command = ":PSTatistic:BANDwidth {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(info_bw, "MHz"))
        center_command = "FREQ:CENTER {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(C_freq, "MHz"))
        center_command = ":PSTatistic:BANDwidth {0:.2f} {1}\n"
        self.N9000a.write(center_command.format(info_bw, "MHz"))
        offset_command = "DISP:WIND:TRAC:Y:RLEV:OFFS {0:.2f} {1}\n"
        self.N9000a.write(offset_command.format(offset, "dB"))
        self.N9000a.write(":INIT:CONT OFF\n")
        self.N9000a.write("*WAI\n")

    def close(self):
            self.N9000a.close()

    def make_single_sweep(self):
        self.N9000a.write(":INIT:CONT OFF\n")
        self.N9000a.write(":INIT:IMM\n")
        self.N9000a.write("*OPC\n")
        self.N9000a.write("*WAI\n")
        #print(self.N9000a.query("SENS:SWE:TIME?\n")) #time of a speed
        #self.N9000a.write("*SRE 0 \n"")
        #self.N9000a.write("*CLS\n"")
    def make_cont_sweep(self):
        self.N9000a.write(":INIT:CONT ON\n")
        #self.N9000a.write(":INIT:IMM\n")
        #self.N9000a.write("*OPC\n")
        self.N9000a.write("*WAI\n")
        #print(self.N9000a.query("SENS:SWE:TIME?\n")) #time of a speed
        #self.N9000a.write("*SRE 0 \n"")
        #self.N9000a.write("*CLS\n"")

    def copy_picture1(self,filname):
        time.sleep(2)
        self.N9000a.write("MMEM:STOR:SCR:THEM TDC\n") #FCOL

        xx1=":MMEM:STOR:SCR \"C:\Temp\{0}.png\"\n"
        #print("fil:",xx1.format(filname))
        self.N9000a.write(xx1.format(filname))
        self.N9000a.write("*OPC\n")

        xx2="MMEM:DATA? \"C:\Temp\{0}.png\"\n"
        self.N9000a.write(xx2.format(filname))
        capture = self.N9000a.binblockread(1) #":MMEM:DATA? \"c:\Temp\pic1.png\"\n")#, datatype='c',is_big_endian=True) #,container=list)#,
        print('file: {0}.png'.format(filname))
        #with open('pic4.png', 'wb') as fp:
        with open('{0}.png'.format(filname), 'wb') as fp:
            for byte in capture:
             fp.write(byte)
        fp.close()
        #print(len(capture))
        #print(capture)
        self.N9000a.query("*CLS\n")
        self.N9000a.write(":MMEM:DEL \"C:\Temp\{0}.png\"\n".format(filname))

    def N9000_data(self,filname):
        time.sleep(2)
        xx1=":MMEM:STOR:results \"C:\Temp\{0}.csv\"\n"
        #print("fil:",xx1.format(filname))
        self.N9000a.write(xx1.format(filname))

        self.N9000a.write("*OPC\n")

        xx2="MMEM:DATA? \"C:\Temp\{0}.csv\"\n"
        self.N9000a.write(xx2.format(filname))
        capture = self.N9000a.binblockread(1) #":MMEM:DATA? \"c:\Temp\pic1.png\"\n")#, datatype='c',is_big_endian=True) #,container=list)#,
        print('file: {0}.csv'.format(filname))
        #with open('pic4.png', 'wb') as fp:
        #ascii = capture.encode('ascii')
        with open('{0}.csv'.format(filname), 'wb') as f:
            f.write(capture)
        f.close()
        self.N9000a.query("*CLS\n")
        self.N9000a.write(":MMEM:DEL \"C:\Temp\{0}.csv\"\n".format(filname))




    def save_spectrum(self, filname,trace,S_freq,C_freq,points):
        #get trace, works on in spectrum analyzer mode
        filename=filname+".csv"
        trace_query = ":TRACe:DATA?  TRACE{0}"
        #check that trace is either 1, 2 or 3
        if trace in (1,2,3):
            xx=self.N9000a.query(trace_query.format(trace))
            xx=np.fromstring( xx, dtype=np.float, sep=',' )
        #open file and save data

            freq= np.linspace(float(C_freq-0.5*S_freq),float(C_freq+0.5*S_freq),int(points))
            dat=np.column_stack((freq,xx))
            #print(dat)
            np.savetxt(filename, dat, delimiter=",")
            print("File: ",filename)

    def iq_setup1(self,myfreq):
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 8\n"
        self.N9000a.write(sa)
        sa = ":INITiate:SPECtrum\n" #:INITiate:WAVeform\n" #:
        self.N9000a.write(sa)
        self.N9000a.write(":INIT:CONT ON\n")
        #xx=self.N9000a.query("SPEC:SRAT?\n")
        self.N9000a.write("SPEC:FREQ:SPAN 10 MHZ\n") #span bw
        #sampling rate S_rate
        #time slot =Res_Bw/S_rate
        #self.N9000a.write("SPEC:BAND 10 kHZ\n") #res bw
        self.N9000a.write("SPEC:FFT:LENG:AUTO 0\n") #res bw
        self.N9000a.write("SPEC:DIF:BAND 10 MHZ\n") #res bw
        self.N9000a.write("SPEC:FFT:LENG 64384\n") #span bw
        self.N9000a.write("SPEC:FFT:WIND:LENG 64384\n") #span bw
        xx=self.N9000a.query("SPEC:SRAT?\n")
        print(float(xx))
        #sampling rate is 15MHz
        #usable I/Q BW=0.8 Sample rate=0.8*15=12MHz
        #sample rate=FEC*N*symbol rate (power(2,N=2) for QPSK)
        #sample rate=symbol rate when FEC =0.5 and QPSK
        #sample rate=12MHz
        #maximum span=20*sym_rate/1.28=15*sym_rate
        #minimum span~sym_rate*(1+apha)~sym_rate*1.3


        #so for symbol=8.3MHz give a bW of 10MHz
        #self.N9000a.write("FCAP:LENG 1024\n")
        #self.N9000a.write("FCAP:BLOCK 8\n")
        #self.N9000a.write("INIT:FCAP\n")
        #self.N9000a.write("*OPC\n")
        #self.N9000a.write("INIT:FCAP\n")
        #maxl=self.N9000a.query("FCAP:LENG? MAX\n")
        #print("1")

        #time.sleep(.2)
        #print(self.N9000a.query("FETCH:FCAP?\n"))
        #self.N9000a.write("FETCH:FCAP?\n")
        #print(self.N9000a.binblockread(1))

        #m_time=maxl*1.0/s_rate
        #req_time=m_time
        #req_points=m_time*S_rate
    def loopTillComplete(self):
        print(self.N9000a.query("*OPC?\n"))
        while float(self.N9000a.query("*OPC?\n")) !=1:  
            print(self.N9000a.query("*OPC?\n"))
            time.sleep(1);
    def iqwave_setup(self,myfreq,sweep_time=230 ,    DIF=10):
        #Sweep_time in ms
        #DIF digital IF band in MHz
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 8\n"
        self.N9000a.write(sa)
        sa = ":INIT:WAV\n" #:INITiate:WAVeform\n" #:
        self.N9000a.write(sa)
        self.N9000a.write(":INIT:CONT ON\n")
        self.N9000a.write("*WAI\n")
         
        #xx=self.N9000a.query("SPEC:SRAT?\n")
        dB_value=40
        self.N9000a.write("pow:ATT {0:.2f}\n".format(float(dB_value)))
        
        center_command = "FREQ:CENTER {0:.2f} MHZ\n"
        self.N9000a.write(center_command.format(myfreq))

        #time slot =Res_Bw/S_rate
        #self.N9000a.write("SPEC:BAND 10 kHZ\n") #res bw
        self.N9000a.write("DISP:WAV:VIEW IQ\n") #res bw
         #s
         #
        fs=float(self.N9000a.query("SPEC:SRAT?\n"))
        #maxLength=float(self.N9000a.query(":FCAP:LENG? MAX\n"))
        #print(fs)
        #maxLength=4000000
        #print(maxLength)
        #maxTime = maxLength / fs
        #print(maxTime)
        #sweep_time=maxTime
        
        center_command = "WAV:SWE:TIME {0:.2f} ms\n"
        self.N9000a.write(center_command.format(sweep_time))
        self.N9000a.write("WAV:DIF:BAND {0:.2f} MHz\n".format(DIF)) #digital IF  bw
        #fsym=2M sym/s
        #if sweep_time is 0.1s then we 0.2M symbols in that periode
        #1 sym is equal 2 samples so the sample rate shall be > 0.4M
        #1/0.4M->

        #self.N9000a.write("WAV:SWE:TIME 200ms\n") #res bw
        #self.N9000a.write("SPEC:FFT:WIND:LENG 64384\n") #span bw
        #self.loopTillComplete()
        time.sleep(1)
        self.N9000a.write("*WAI\n")
        return float(fs),sweep_time,DIF

        
     
    

        #xx=self.N9000a.query("FETCH:FCAP?\n")
        #print(xx)
        #set up spand frequency to 10MHz
    def NF_meas_converter(self,start,stop,bw,avg,lo,points,mytype="DOWN"):
        #mytype:"Down" for downconverter or "UPC" for upconverter
        self.N9000a.write("*RST\n")
        sa = "INST:NSEL 219\n"
        self.N9000a.write(sa)
        myfreq=2000
        points_command = ":SWE:POIN {0}\n"
        self.N9000a.write(points_command.format(points))

        sa = ":FREQ:STAR {0}{1}\n" #video BW
        self.N9000a.write(sa.format(start,"MHz"))
        sa = ":FREQ:STOP {0}{1}\n" #resolution BW
        self.N9000a.write(sa.format(stop,"MHz"))
        sa = ":BANDWIDTH {0}{1}\n" #resolution BW
        self.N9000a.write(sa.format(bw,"MHz"))
      
        avg_command = ":AVER:COUN {0}\n"
        self.N9000a.write(avg_command.format(avg))
        self.N9000a.write(":AVER ON\n")
       
        self.N9000a.write(":MODE:DUT {0}\n".format(mytype))
        #time.sleep(10)
        self.N9000a.write(":MODE:{0}:LOSC:OFFS USB\n".format(mytype)) #hardcoded upper side band
        self.N9000a.write(":MODE:DUT:LOSC FIX\n")
        
        sa = ":MODE:{0}:LOSCillator:FREQuency {1}{2}\n"
        
        self.N9000a.write(sa.format(mytype,lo,"MHz"))
        self.N9000a.write(":INIT:CONT ON\n")
        
    def NF_meas(self,start,stop,bw,avg,points):
        self.N9000a.write("*RST\n")
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
