"""
Main Script as per BRO S_Band Check_Out Reporting Generator:
4 sets of 4 LNA to be verified:
S_BAND_LNA
    4xNoise_Figure
    4xSpurious

X_BAND_RECEIVER
    4xS_PARAMETERS: Magnitude and Unwrapped Phase
    4x
"""

import sys, os

#from Tools.scripts.patchcheck import status
#from pyvisa.constants import VI_ERROR_BERR, VI_ATTR_WIN_BASE_ADDR_32, VI_ATTR_WIN_BASE_ADDR_64

sys.path.insert(1, 'C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include')
import time
import pickle
### comming from Pickles module

import lna_aadetect as aa_function
import S_BAND_Identification as LNA
import NF_SBAND as NF
import GAIN_PHASE_S_BAND as GAIN
import SPURIOUS_SBAND as SP
import class_VNA as vna
from datetime import datetime
from skrf import Network
import matplotlib.pyplot as plt
from skrf import plotting
from skrf.plotting import save_all_figs
import os
from time import sleep

'''
Class Object Initialisation
'''
VNA_P1_BEFORE           =   vna.VNA()
VNA_P2_BEFORE           =   vna.VNA()
VNA_P3_BEFORE           =   vna.VNA()
VNA_P4_BEFORE           =   vna.VNA()
VNA_P5_BEFORE           =   vna.VNA()
VNA_P6_BEFORE           =   vna.VNA()

VNA_P1_AFTER           =   vna.VNA()
VNA_P2_AFTER           =   vna.VNA()
VNA_P3_AFTER           =   vna.VNA()
VNA_P4_AFTER           =   vna.VNA()
VNA_P5_AFTER           =   vna.VNA()
VNA_P6_AFTER           =   vna.VNA()

VNA_TEMP        =   vna.VNA()
VNA_TEMP_CONCAT =   vna.VNA()
UW_Phase_Table  =   []
Phase_Reference =   1 # Branche reference - 1
SN_NAME = 'Ser_no_16'
SN_NAME_DIRECTORY ="111130-16"
ANTENNA_BEFORE_GLUE            = [SN_NAME+'_Sj1x_Sj3x.S2P',SN_NAME+'_Sj1x_Sj3x.S2P', SN_NAME+'_Sj1x_Sj4x.S2P', SN_NAME+'_Sj2x_Sj3x.S2P', SN_NAME+'_Sj2x_Sj4x.S2P',SN_NAME+'_Sj3x_Sj4x.S2P' ]
ANTENNA_AFTER_GLUE             = [SN_NAME+'_Sj1x_Sj3x.S2P',SN_NAME+'_Sj1x_Sj3x.S2P', SN_NAME+'_Sj1x_Sj4x.S2P', SN_NAME+'_Sj2x_Sj3x.S2P', SN_NAME+'_Sj2x_Sj4x.S2P',SN_NAME+'_Sj3x_Sj4x.S2P' ]

Path_to_S2P_AFTER            =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\"+SN_NAME_DIRECTORY+"\\internal\\"
Path_to_S2P_BEFORE           =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\"+SN_NAME_DIRECTORY+"\\internal\\"
Path_to_WORKING_DIRECTORY_BEFORE_GLUE   =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\"+SN_NAME_DIRECTORY+"\\SN"+SN_NAME_DIRECTORY+"\\"
Path_to_WORKING_DIRECTORY_AFTER_GLUE    =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\"+SN_NAME_DIRECTORY+"\\SN"+SN_NAME_DIRECTORY+"\\"
Path_to_WORKING_DIRECTORY_COMPARISON    =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\"+SN_NAME_DIRECTORY+"\\SN"+SN_NAME_DIRECTORY+"_COMPARISON\\"
X_band_RL_Antenna_SPEC = -15
X_band_COUPLING_Antenna_SPEC = -15
X_band_COUPLING_Antenna_3_1_SPEC = -15
_frequency_band_lowest_limit_MHz    =   9.200*1e9
_frequency_band_highest_limit_MHz   =   9.420*1e9


VNA_P1_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[0])
VNA_P2_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[1])
VNA_P3_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[2])
VNA_P4_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[3])
VNA_P5_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[4])
VNA_P6_BEFORE.change_name(Path_to_S2P_BEFORE+ANTENNA_BEFORE_GLUE[5])

VNA_P1_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[0])
VNA_P2_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[1])
VNA_P3_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[2])
VNA_P4_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[3])
VNA_P5_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[4])
VNA_P6_AFTER.change_name(Path_to_S2P_AFTER+ANTENNA_AFTER_GLUE[5])

VNA_P1_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)
VNA_P2_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)
VNA_P3_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)
VNA_P4_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)
VNA_P5_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)
VNA_P6_BEFORE.change_working_directory(Path_to_WORKING_DIRECTORY_BEFORE_GLUE)

VNA_P1_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)
VNA_P2_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)
VNA_P3_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)
VNA_P4_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)
VNA_P5_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)
VNA_P6_AFTER.change_working_directory(Path_to_WORKING_DIRECTORY_AFTER_GLUE)

VNA_TEMP_CONCAT.change_working_directory(Path_to_WORKING_DIRECTORY_COMPARISON)



[s11_P1, s11_P2, s11_P3, s11_P4,s11_P5,s11_P6,Frequency_Vector] = VNA_TEMP.concat_S_parameter_ports(VNA_P1_AFTER,VNA_P2_AFTER,VNA_P3_AFTER,VNA_P4_AFTER,VNA_P5_AFTER, VNA_P6_AFTER,"s11")
[s22_P1, s22_P2, s22_P3, s22_P4,s22_P5,s22_P6,Frequency_Vector] = VNA_TEMP.concat_S_parameter_ports(VNA_P1_AFTER,VNA_P2_AFTER,VNA_P3_AFTER,VNA_P4_AFTER,VNA_P5_AFTER, VNA_P6_AFTER, "s22")
[s12_P1, s12_P2, s12_P3, s12_P4,s12_P5,s12_P6,Frequency_Vector] = VNA_TEMP.concat_S_parameter_ports(VNA_P1_AFTER,VNA_P2_AFTER,VNA_P3_AFTER,VNA_P4_AFTER,VNA_P5_AFTER, VNA_P6_AFTER, "s12")
[s21_P1, s21_P2, s21_P3, s21_P4,s21_P5,s21_P6,Frequency_Vector] = VNA_TEMP.concat_S_parameter_ports(VNA_P1_AFTER,VNA_P2_AFTER,VNA_P3_AFTER,VNA_P4_AFTER,VNA_P5_AFTER, VNA_P6_AFTER, "s21")

[ status, _Performance_Return_Loss_J1X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s11_P1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_J1X_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s11_P1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_J2X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s11_P2, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_J2X_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s11_P2, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_J3X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s11_P3, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_J3X_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s11_P3, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_J4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s11_P4, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_J4X_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s11_P4, _frequency_band_highest_limit_MHz)


[ status, _Performance_Coupling_Loss_J1XJ2X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J1XJ2X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_J1XJ3X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P2, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J1XJ3X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P2, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_J1XJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P3, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J1XJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P3, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_J2XJ3X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P4, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J2XJ3X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P4, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_J2XJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P5, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J2XJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P5, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_J3XJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P6, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_J3XJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P6, _frequency_band_highest_limit_MHz)


print('RL_low_bound_J1X:',"{:.2f}".format(_Performance_Return_Loss_J1X_low_freq),' dB')
print('RL_high_bound_J1X:',"{:.2f}".format(_Performance_Return_Loss_J1X_high_freq),' dB')
print('RL_low_bound_J2X:',"{:.2f}".format(_Performance_Return_Loss_J2X_low_freq),' dB')
print('RL_high_bound_J2X:',"{:.2f}".format(_Performance_Return_Loss_J2X_high_freq),' dB')
print('RL_low_bound_J3X:',"{:.2f}".format(_Performance_Return_Loss_J3X_low_freq),' dB')
print('RL_high_bound_J3X:',"{:.2f}".format(_Performance_Return_Loss_J3X_high_freq),' dB')
print('RL_low_bound_J4X:',"{:.2f}".format(_Performance_Return_Loss_J4X_low_freq),' dB')
print('RL_high_bound_J4X:',"{:.2f}".format(_Performance_Return_Loss_J4X_high_freq),' dB')

print('COUPLING_low_bound_J1XJ2X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ2X_low_freq),' dB')
print('COUPLING_high_bound_J1XJ2X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ2X_high_freq),' dB')
print('COUPLING_low_bound_J1XJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ3X_low_freq),' dB')
print('COUPLING_high_bound_J1XJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ3X_high_freq),' dB')
print('COUPLING_low_bound_J1XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ3X_low_freq),' dB')
print('COUPLING_high_bound_J1XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J1XJ3X_high_freq),' dB')
print('COUPLING_low_bound_J2XJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_J2XJ3X_low_freq),' dB')
print('COUPLING_high_bound_J2XJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_J2XJ3X_high_freq),' dB')
print('COUPLING_low_bound_J2XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J2XJ4X_low_freq),' dB')
print('COUPLING_high_bound_J2XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J2XJ4X_high_freq),' dB')
print('COUPLING_low_bound_J3XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J3XJ4X_low_freq),' dB')
print('COUPLING_high_bound_J3XJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_J3XJ4X_high_freq),' dB')


_s_param_list   =   ['S11', 'S22', 'S21', 'S12']
_legend_list    =   ['RETURN LOSS in dB - '+ SN_NAME_DIRECTORY,'COUPLING in dB - '+ SN_NAME_DIRECTORY, 'RETURN LOSS in dB - '+ SN_NAME_DIRECTORY, 'COUPLING in dB - '+ SN_NAME_DIRECTORY]
_type_of_plot   =   ['magnitude_dB']
_port_naming    =   ['PORTJ1X','PORTJ2X','PORTJ3X','PORTJ4X','J1XtoJ2X','J1XtoJ3X','J1XtoJ4X','J2XtoJ3X','J2XtoJ4X','J3XtoJ5X']

### Performance in Return Loss Before stand alone
VNA_P1_BEFORE.save(_port_naming[0]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P4_BEFORE.save(_port_naming[1]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P6_BEFORE.save(_port_naming[3]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P4_BEFORE.save(_port_naming[2]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1], X_band_RL_Antenna_SPEC)

### Performance in Return Loss After stand alone
VNA_P1_AFTER.save(_port_naming[0]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P4_AFTER.save(_port_naming[1]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P6_AFTER.save(_port_naming[3]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_P4_AFTER.save(_port_naming[2]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1], X_band_RL_Antenna_SPEC)

### Performance in Coupling loss Before
VNA_P1_BEFORE.save(_port_naming[0]+_port_naming[1]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)
VNA_P2_BEFORE.save(_port_naming[0]+_port_naming[2]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)
VNA_P3_BEFORE.save(_port_naming[0]+_port_naming[3]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)
VNA_P4_BEFORE.save(_port_naming[1]+_port_naming[2]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)
VNA_P5_BEFORE.save(_port_naming[1]+_port_naming[3]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)
VNA_P6_BEFORE.save(_port_naming[2]+_port_naming[3]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], X_band_COUPLING_Antenna_SPEC)

### Performance in Return Loss Before and After on same plots
VNA_TEMP_CONCAT.save_2_ports(VNA_P1_BEFORE,_port_naming[0]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P1_AFTER,_port_naming[0]+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P4_BEFORE,_port_naming[1]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P4_AFTER,_port_naming[1]+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P6_BEFORE,_port_naming[2]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P6_AFTER,_port_naming[2]+_legend_list[2], _type_of_plot[0], _s_param_list[0], X_band_RL_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P3_BEFORE,_port_naming[3]+_legend_list[0], _type_of_plot[0], _s_param_list[1],VNA_P3_AFTER,_port_naming[3]+_legend_list[2], _type_of_plot[0], _s_param_list[1], X_band_RL_Antenna_SPEC)

### Coupling Loss Before and After on same plots
VNA_TEMP_CONCAT.save_2_ports(VNA_P1_BEFORE,'J1XtoJ2X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P1_AFTER,'J1XtoJ2X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P2_BEFORE,'J1XtoJ3X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P2_AFTER,'J1XtoJ3X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_3_1_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P3_BEFORE,'J1XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P3_AFTER,'J1XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P4_BEFORE,'J2XtoJ3X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P4_AFTER,'J2XtoJ3X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P5_BEFORE,'J2XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P5_AFTER,'J2XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_SPEC)
VNA_TEMP_CONCAT.save_2_ports(VNA_P6_BEFORE,'J3XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P6_AFTER,'J3XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], X_band_COUPLING_Antenna_3_1_SPEC)


#VNA_P3_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P4_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P5_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
