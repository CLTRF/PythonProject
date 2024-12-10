#section 4.6 BIAS optimization
#from rssd.SMW_Common import VSG
import instruments as ik

#import instruments as ik
import sys,os
# Bias optimization using
# -r&S power meter
# -SMU200A generator
# section bias optimization
#rm = visa.ResourceManager()


class SMU200:
#smu200 generator
    def __init__(self,SMU200host):
        self.SMU200= ik.generic_scpi.SCPIInstrument.open_tcpip(SMU200host, 5025)
        info= self.SMU200.query("*IDN?")
        print("Info:"+ str(info))
        self.SMU200.write("*RST\n")


    def single_freq(self,mypwd,myfreq):
        #check if power sweep
        pow_command = ":SOUR:POW {0:.2f} {1}\n"
        freq_command = ":SOUR:FREQ {0:.2f} {1}\n"
        #self.SMU200.write(freq_command.format(myfreq, "MHz"))
        self.SMU200.write(pow_command.format(mypwd, "dBm"))
        self.SMU200.write(freq_command.format(myfreq, "MHz"))

    def close(self):
        self.SMU200.close()

    def RF_on(self):
        self.SMU200.write(':OUTP ON\n') #output1=path A, output2=path B,

    def RF_off(self):
        self.SMU200.write(':OUTP OFF\n') #output1=path A, output2=path B,
    def test(self):
        self.SMU200.write('FREQ?\n') #output1=path A, output2=path B,
    def ARB_off(self):
        self.SMU200.write(':SOUR:BB:ARB:STATE ON\n')

    def ARB_load(self,myMod):
        #Turn on Arb & IQ Mod
        if myMod!='none':
            if myMod=='Qpsk':
                self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\dvb_6mhz.wv'\n ")
            if myMod=='8PSK':
                self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\dvb_6mhz.wv'\n ")
            if myMod=='APSK16':
                self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\dvb_6mhz.wv'\n ")
            if myMod=='APSK32':
                self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\dvb_6mhz.wv'\n ")

            #Turn on Arb
            self.SMU200.write(':SOUR:BB:ARB:STATE ON\n')
        #setpower on
            self.SMU200.write(':OUTP ON\n') #output1=path A, output2=path B,
    def modcon_DVB_S2(self,modcon,bitrate):
        if 0<modcon<29:
            self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\modcon_DVB_S2\modcon{:d}.wv'\n ".format(int(modcon)))
            self.SMU200.write(':SOUR:BB:ARB:STATE ON\n')
            self.SMU200.write(":SOUR:BB:ARB:CLOCK {:f}\n ".format(bitrate*1000000))
        if modcon==100:
            self.SMU200.write(":SOUR:BB:ARB:WAV:SEL 'c:\TEMP\modcon_DVB_S2\motch.wv'\n ")
            self.SMU200.write(':SOUR:BB:ARB:STATE ON\n')
            self.SMU200.write(":SOUR:BB:ARB:CLOCK {:f}\n ".format(bitrate*1000000))
        #self.SMU200.write(":SOUR:BB:ARB:CLOCK 100000\n")
        self.SMU200.write(':OUTP ON\n') #ou
    def mod_digital(self,bitrate):
        #self.SMU200.write(':SOUR:BB:DM:SOUR ZERO\n')
        #self.SMU200.write(':SOUR:BB:DM:SOUR ONE\n')

        self.SMU200.write(':SOUR:BB:DM:PRBS 9\n')
        self.SMU200.write(':SOUR:BB:DM:COD OFF\n')
        self.SMU200.write(':SOUR:BB:DM:FORM QPSK\n')
        self.SMU200.write(':SOUR:BB:DM:FILT:TYPE GAUS\n')
        #self.SMU200.write(':SOUR:BB:DM:FILT:PAR 0.2\n')

        self.SMU200.write('BB:DM:SRAT {0} MHz\n'.format(bitrate)) #ou

        self.SMU200.write(':SOUR:BB:DM:STATE ON\n')

        self.SMU200.write(':OUTP ON\n') #ou


    def copy_picture1(self,filname):

        self.SMU200.write("HCOP:DEV:LANG PNG\n")
        self.SMU200.write("HCOP:DATA?\n")

        capture = self.SMU200.binblockread(1) #":MMEM:DATA? \"c:\Temp\pic1.png\"\n")#, datatype='c',is_big_endian=True) #,container=list)#,
        print('file: {0}.png'.format(filname))
        #with open('pic4.png', 'wb') as fp:
        with open('{0}.png'.format(filname), 'wb') as fp:
            for byte in capture:
             fp.write(byte)
        fp.close()
        #print(len(capture))
        #print(capture)
        self.SMU200.query("*CLS\n")


##############################################################################
#                           main program
##############################################################################
#TCP settings
#SMU200_host = '10.0.9.18'

#SMU200 settings
#BB_Mod=['none','Qpsk','8PSK','APSK16','APSK32']
#if_freq=1200 #if frequency in Mhz
#if_pow=0 #if power in dBm
#SMU200_on='false'

#SMU200b=SMU200(SMU200_host)

#SMU200b.single_freq(if_pow,if_freq)

#SMU200b.ARB_load(BB_Mod[1])
#import time
#time.sleep(2)

#
#SMU200b.RF_on()
#SMU200b.copy_picture1("pic0")

#SMU200b.RF_off()
