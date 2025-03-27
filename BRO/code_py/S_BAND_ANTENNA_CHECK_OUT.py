"""
Main Script as per BRO S_Band Check_Out Reporting Generator:
4 sets of 4 LNA to be verified:
S_BAND_LNA
    4xNoise_Figure
    4xSpurious

S_BAND_RECEIVER
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
VNA_P1_111720_1           =   vna.VNA()
VNA_P2_111720_1           =   vna.VNA()
VNA_P3_111720_1           =   vna.VNA()
VNA_P4_111720_1           =   vna.VNA()
VNA_P5_111720_1           =   vna.VNA()
VNA_P6_111720_1           =   vna.VNA()
VNA_P7_111720_1           =   vna.VNA()

VNA_P1_111720_2           =   vna.VNA()
VNA_P2_111720_2           =   vna.VNA()
VNA_P3_111720_2           =   vna.VNA()
VNA_P4_111720_2           =   vna.VNA()
VNA_P5_111720_2           =   vna.VNA()
VNA_P6_111720_2           =   vna.VNA()
VNA_P7_111720_2           =   vna.VNA()

VNA_TEMP        =   vna.VNA()
VNA_TEMP_CONCAT =   vna.VNA()
UW_Phase_Table  =   []
Phase_Reference =   1 # Branche reference - 1
ANTENNA_111720_1            = ['111720-1_SJ0x_Sj1x.S2P', '111720-1_SJ1x_Sj2x.S2P', '111720-1_SJ1x_Sj3x.S2P', '111720-1_SJ1x_Sj4x.S2P','111720-1_SJ2x_Sj3x.S2P', '111720-1_SJ2x_Sj4x.S2P', '111720-1_SJ3x_Sj4x.S2P' ]
ANTENNA_111720_2            = ['111720-2_SJ0x_Sj1x.S2P', '111720-2_SJ1x_Sj2x.S2P', '111720-2_SJ1x_Sj3x.S2P', '111720-2_SJ1x_Sj4x.S2P','111720-2_SJ2x_Sj3x.S2P', '111720-2_SJ2x_Sj4x.S2P', '111720-2_SJ3x_Sj4x.S2P' ]

Path_to_S2P_111720_1                    =   "H:\\DATA_WARE_HOUSE\\LNA_Antenna\\111720_1\\internal\\"
Path_to_S2P_111720_2                    =   "H:\\DATA_WARE_HOUSE\\LNA_Antenna\\111720_2\\internal\\"
Path_to_WORKING_DIRECTORY_111720_1      =   "H:\\DATA_WARE_HOUSE\\LNA_Antenna\\DataWareHouse\\111720_1\\"
Path_to_WORKING_DIRECTORY_111720_2      =   "H:\\DATA_WARE_HOUSE\\LNA_Antenna\\DataWareHouse\\111720_2\\"
Path_to_WORKING_DIRECTORY_COMPARISON    =   "H:\\DATA_WARE_HOUSE\\LNA_Antenna\\DataWareHouse\\COMPARISON"
S_BAND_Antenna_SPEC = -15
S_BAND_COUPLING_Antenna_SPEC = -15
S_BAND_COUPLING_Antenna_3_1_SPEC = -15
_frequency_band_lowest_limit_MHz    =   3.000*1e9
_frequency_band_highest_limit_MHz   =   3.100*1e9


VNA_P1_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[0])
VNA_P2_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[1])
VNA_P3_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[2])
VNA_P4_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[3])
VNA_P5_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[4])
VNA_P6_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[5])
VNA_P7_111720_1.change_name(Path_to_S2P_111720_1+ANTENNA_111720_1[6])

VNA_P1_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[0])
VNA_P2_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[1])
VNA_P3_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[2])
VNA_P4_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[3])
VNA_P5_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[4])
VNA_P6_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[5])
VNA_P7_111720_2.change_name(Path_to_S2P_111720_2+ANTENNA_111720_2[6])

VNA_P1_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P2_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P3_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P4_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P5_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P6_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)
VNA_P7_111720_1.change_working_directory(Path_to_WORKING_DIRECTORY_111720_1)

VNA_P1_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P2_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P3_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P4_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P5_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P6_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)
VNA_P7_111720_2.change_working_directory(Path_to_WORKING_DIRECTORY_111720_2)

VNA_TEMP_CONCAT.change_working_directory(Path_to_WORKING_DIRECTORY_COMPARISON)

[s11_P1_111720_1, s11_P2_111720_1, s11_P3_111720_1, s11_P4_111720_1,s11_P5_111720_1,s11_P6_111720_1,s11_P7_111720_1, Frequency_Vector] = VNA_TEMP.concat_S_parameter_7_ports(VNA_P1_111720_1,VNA_P2_111720_1,VNA_P3_111720_1,VNA_P4_111720_1,VNA_P5_111720_1, VNA_P6_111720_1,VNA_P7_111720_1,"s11")
[s22_P1_111720_1, s22_P2_111720_1, s22_P3_111720_1, s22_P4_111720_1,s22_P5_111720_1,s22_P6_111720_1,s22_P7_111720_1, Frequency_Vector] = VNA_TEMP.concat_S_parameter_7_ports(VNA_P1_111720_1,VNA_P2_111720_1,VNA_P3_111720_1,VNA_P4_111720_1,VNA_P5_111720_1, VNA_P6_111720_1,VNA_P7_111720_1,"s22")
[s12_P1_111720_1, s12_P2_111720_1, s12_P3_111720_1, s12_P4_111720_1,s12_P5_111720_1,s12_P6_111720_1,s12_P7_111720_1, Frequency_Vector] = VNA_TEMP.concat_S_parameter_7_ports(VNA_P1_111720_1,VNA_P2_111720_1,VNA_P3_111720_1,VNA_P4_111720_1,VNA_P5_111720_1, VNA_P6_111720_1,VNA_P7_111720_1,"s12")
[s21_P1_111720_1, s21_P2_111720_1, s21_P3_111720_1, s21_P4_111720_1,s12_P5_111720_1,s21_P6_111720_1,s21_P7_111720_1, Frequency_Vector] = VNA_TEMP.concat_S_parameter_7_ports(VNA_P1_111720_1,VNA_P2_111720_1,VNA_P3_111720_1,VNA_P4_111720_1,VNA_P5_111720_1, VNA_P6_111720_1,VNA_P7_111720_1,"s21")

[ status, _Performance_Return_Loss_SJ0x_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s11_P1_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_SJ0x_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s11_P1_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_SJ1x_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s22_P2_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_SJ1x_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s22_P2_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_SJ2x_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s22_P2_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_SJ2x_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s22_P2_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_SJ3x_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s22_P3_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_SJ3x_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s22_P3_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Return_Loss_SJ4x_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s22_P6_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Return_Loss_SJ4x_high_freq]   = GAIN.find_value_at_spec(Frequency_Vector, s22_P6_111720_1, _frequency_band_highest_limit_MHz)

[ status, _Performance_Coupling_Loss_SJ0xJ1X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P1_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ0xJ1X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P1_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ2X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P2_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ2X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P2_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ3X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P3_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ3X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P3_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P4_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ1xJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P4_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ2xJ3X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P5_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ2xJ3X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P5_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ2xJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P6_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ2xJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P6_111720_1, _frequency_band_highest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ3xJ4X_low_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P7_111720_1, _frequency_band_lowest_limit_MHz)
[ status, _Performance_Coupling_Loss_SJ3xJ4X_high_freq]    = GAIN.find_value_at_spec(Frequency_Vector, s12_P7_111720_1, _frequency_band_highest_limit_MHz)


print('RL_low_bound_SJ1x:',"{:.2f}".format(_Performance_Return_Loss_SJ1x_low_freq),' dB')
print('RL_high_bound_SJ1x:',"{:.2f}".format(_Performance_Return_Loss_SJ1x_high_freq),' dB')
print('RL_low_bound_SJ2x:',"{:.2f}".format(_Performance_Return_Loss_SJ2x_low_freq),' dB')
print('RL_high_bound_SJ2x:',"{:.2f}".format(_Performance_Return_Loss_SJ2x_high_freq),' dB')
print('RL_low_bound_SJ3x:',"{:.2f}".format(_Performance_Return_Loss_SJ3x_low_freq),' dB')
print('RL_high_bound_SJ3x:',"{:.2f}".format(_Performance_Return_Loss_SJ3x_high_freq),' dB')
print('RL_low_bound_SJ4x:',"{:.2f}".format(_Performance_Return_Loss_SJ4x_low_freq),' dB')
print('RL_high_bound_SJ4x:',"{:.2f}".format(_Performance_Return_Loss_SJ4x_high_freq),' dB')

print('COUPLING_low_bound_SJ1xJ2X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ2X_low_freq),' dB')
print('COUPLING_high_bound_SJ1xJ2X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ2X_high_freq),' dB')
print('COUPLING_low_bound_SJ1xJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ3X_low_freq),' dB')
print('COUPLING_high_bound_SJ1xJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ3X_high_freq),' dB')
print('COUPLING_low_bound_SJ1xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ3X_low_freq),' dB')
print('COUPLING_high_bound_SJ1xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ1xJ3X_high_freq),' dB')
print('COUPLING_low_bound_SJ2xJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ2xJ3X_low_freq),' dB')
print('COUPLING_high_bound_SJ2xJ3X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ2xJ3X_high_freq),' dB')
print('COUPLING_low_bound_SJ2xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ2xJ4X_low_freq),' dB')
print('COUPLING_high_bound_SJ2xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ2xJ4X_high_freq),' dB')
print('COUPLING_low_bound_SJ3xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ3xJ4X_low_freq),' dB')
print('COUPLING_high_bound_SJ3xJ4X:',"{:.2f}".format(_Performance_Coupling_Loss_SJ3xJ4X_high_freq),' dB')


_s_param_list   =   ['S11', 'S22', 'S21', 'S12']
_legend_list    =   ['RETURN LOSS in dB - ANTENNA 111720_1','COUPLING in dB - ANTENNA 111720_1', 'RETURN LOSS in dB - ANTENNA 111720_2', 'COUPLING in dB - ANTENNA 111720_2']
_type_of_plot   =   ['magnitude_dB']
_port_naming    =   ['PORTSJ0x','PORTSJ1x','PORTSJ2x','PORTSJ3x','PORTSJ4x','J0XtoJ1X','J1XtoJ2X','J1XtoJ3X','J1XtoJ4X','J2XtoJ3X','J2XtoJ4X','J3XtoJ5X']

### Performance in Return Loss 111720_1 stand alone
VNA_P1_111720_1.save(_port_naming[0]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0], S_BAND_Antenna_SPEC)
VNA_P1_111720_1.save(_port_naming[1]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P2_111720_1.save(_port_naming[2]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P3_111720_1.save(_port_naming[3]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P6_111720_1.save(_port_naming[4]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)

### Performance in Return Loss 111720_2 stand alone
VNA_P1_111720_2.save(_port_naming[0]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0], S_BAND_Antenna_SPEC)
VNA_P1_111720_2.save(_port_naming[1]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P2_111720_2.save(_port_naming[2]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P3_111720_2.save(_port_naming[3]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)
VNA_P6_111720_2.save(_port_naming[4]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)

### Performance in Coupling loss 111720_1
VNA_P1_111720_1.save(_port_naming[0]+_port_naming[1]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P2_111720_1.save(_port_naming[1]+_port_naming[2]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P5_111720_1.save(_port_naming[2]+_port_naming[3]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P7_111720_1.save(_port_naming[3]+_port_naming[4]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P4_111720_1.save(_port_naming[1]+_port_naming[4]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P6_111720_1.save(_port_naming[2]+_port_naming[4]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P3_111720_1.save(_port_naming[1]+_port_naming[3]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)

### Performance in Coupling loss 111720_2
VNA_P1_111720_2.save(_port_naming[0]+_port_naming[1]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P2_111720_2.save(_port_naming[1]+_port_naming[2]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P5_111720_2.save(_port_naming[2]+_port_naming[3]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P7_111720_2.save(_port_naming[3]+_port_naming[4]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P4_111720_2.save(_port_naming[1]+_port_naming[4]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P6_111720_2.save(_port_naming[2]+_port_naming[4]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)
VNA_P3_111720_2.save(_port_naming[1]+_port_naming[3]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[3], S_BAND_COUPLING_Antenna_SPEC)

### Performance in Return Loss 111720_1 and 111720_2 on same plots
#VNA_TEMP_CONCAT.save_2_ports(VNA_P1_111720_1,_port_naming[0]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P1_111720_2,_port_naming[0]+_legend_list[2], _type_of_plot[0], _s_param_list[0], S_BAND_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P4_111720_1,_port_naming[1]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P4_111720_2,_port_naming[1]+_legend_list[2], _type_of_plot[0], _s_param_list[0], S_BAND_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P6_111720_1,_port_naming[2]+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P6_111720_2,_port_naming[2]+_legend_list[2], _type_of_plot[0], _s_param_list[0], S_BAND_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P3_111720_1,_port_naming[3]+_legend_list[0], _type_of_plot[0], _s_param_list[1],VNA_P3_111720_2,_port_naming[3]+_legend_list[2], _type_of_plot[0], _s_param_list[1], S_BAND_Antenna_SPEC)

### Coupling Loss 111720_1 and 111720_2 on same plots
#VNA_TEMP_CONCAT.save_2_ports(VNA_P1_111720_1,'J1XtoJ2X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P1_111720_2,'J1XtoJ2X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P2_111720_1,'J1XtoJ3X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P2_111720_2,'J1XtoJ3X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_3_1_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P3_111720_1,'J1XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P3_111720_2,'J1XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P4_111720_1,'J2XtoJ3X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P4_111720_2,'J2XtoJ3X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P5_111720_1,'J2XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P5_111720_2,'J2XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_SPEC)
#VNA_TEMP_CONCAT.save_2_ports(VNA_P6_111720_1,'J3XtoJ4X '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P6_111720_2,'J3XtoJ4X '+_legend_list[3], _type_of_plot[0], _s_param_list[2], S_BAND_COUPLING_Antenna_3_1_SPEC)


#VNA_P3_111720_1.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P4_111720_1.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P5_111720_1.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
