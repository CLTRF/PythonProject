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
ANTENNA_BEFORE_GLUE            = ['111129-5_1a.S2P', '111129-5_2a.S2P', '111129-5_3a.S2P', '111129-5_4a.S2P','111129-5_5a.S2P', '111129-5_6a.S2P' ]
ANTENNA_AFTER_GLUE             = ['111129-10_1a.S2P', '111129-10_2a.S2P', '111129-10_3a.S2P', '111129-10_4a.S2P','111129-10_5a.S2P', '111129-10_6a.S2P' ]

Path_to_S2P_AFTER          =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\efterlim\\"
Path_to_S2P_BEFORE           =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\førlim\\internal\\"
Path_to_WORKING_DIRECTORY_BEFORE_GLUE   =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\BEFORE"
Path_to_WORKING_DIRECTORY_AFTER_GLUE   =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\AFTER"
Path_to_WORKING_DIRECTORY_COMPARISON   =   "H:\\DATA_WARE_HOUSE\\LNB_Antenna\\DataWareHouse\\COMPARISON"

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

[s11_P1, s11_P2, s11_P3, s11_P4,s11_P5,Frequency_Vector] = VNA_TEMP.concat_S_parameter_five_ports(VNA_P1_BEFORE,VNA_P2_BEFORE,VNA_P3_BEFORE,VNA_P4_BEFORE,VNA_P5_BEFORE, "s11")
[s22_P1, s22_P2, s22_P3, s22_P4,s22_P5,Frequency_Vector] = VNA_TEMP.concat_S_parameter_five_ports(VNA_P1_BEFORE,VNA_P2_BEFORE,VNA_P3_BEFORE,VNA_P4_BEFORE,VNA_P5_BEFORE, "s22")
[s12_P1, s12_P2, s12_P3, s12_P4,s12_P5,Frequency_Vector] = VNA_TEMP.concat_S_parameter_five_ports(VNA_P1_BEFORE,VNA_P2_BEFORE,VNA_P3_BEFORE,VNA_P4_BEFORE,VNA_P5_BEFORE, "s12")
[s21_P1, s21_P2, s21_P3, s21_P4,s21_P5,Frequency_Vector] = VNA_TEMP.concat_S_parameter_five_ports(VNA_P1_BEFORE,VNA_P2_BEFORE,VNA_P3_BEFORE,VNA_P4_BEFORE,VNA_P5_BEFORE, "s21")

_s_param_list   =   ['S11', 'S22', 'S21', 'S12']
_legend_list    =   ['RETURN LOSS in dB - Back plate not mounted','COUPLING in dB - Back plate not mounted', 'RETURN LOSS in dB - Back plate mounted', 'COUPLING in dB - Back plate mounted']
_type_of_plot   =   ['magnitude_dB']
_port_naming    =   ['PORT 1a','PORT 2a','PORT 3a','PORT 4a','1a to 2a','1a to 3a','1a to 4a','2a to 3a','2a to 4a','3a to 5a']

### Performance in Return Loss Before stand alone
VNA_P1_BEFORE.save(_port_naming[0]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0])
VNA_P4_BEFORE.save(_port_naming[1]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0])
VNA_P6_BEFORE.save(_port_naming[3]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0])
VNA_P3_BEFORE.save(_port_naming[2]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[3])

### Performance in Return Loss After stand alone
VNA_P1_AFTER.save(_port_naming[0]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_P4_AFTER.save(_port_naming[1]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_P6_AFTER.save(_port_naming[3]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_P3_AFTER.save(_port_naming[2]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[3])

### Performance in Return Loss Before and After on same plots
VNA_TEMP_CONCAT.save_2_ports(VNA_P1_BEFORE,_port_naming[0]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P1_AFTER,_port_naming[0]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_TEMP_CONCAT.save_2_ports(VNA_P4_BEFORE,_port_naming[1]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P4_AFTER,_port_naming[1]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_TEMP_CONCAT.save_2_ports(VNA_P6_BEFORE,_port_naming[2]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[0],VNA_P6_AFTER,_port_naming[2]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[0])
VNA_TEMP_CONCAT.save_2_ports(VNA_P3_BEFORE,_port_naming[3]+' '+_legend_list[0], _type_of_plot[0], _s_param_list[1],VNA_P3_AFTER,_port_naming[3]+' '+_legend_list[2], _type_of_plot[0], _s_param_list[1])

### Coupling Loss Before and After on same plots
VNA_TEMP_CONCAT.save_2_ports(VNA_P1_BEFORE,_port_naming[4]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P1_AFTER,_port_naming[4]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])
VNA_TEMP_CONCAT.save_2_ports(VNA_P2_BEFORE,_port_naming[5]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P2_AFTER,_port_naming[5]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])
VNA_TEMP_CONCAT.save_2_ports(VNA_P3_BEFORE,_port_naming[6]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P3_AFTER,_port_naming[6]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])
VNA_TEMP_CONCAT.save_2_ports(VNA_P4_BEFORE,_port_naming[7]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P4_AFTER,_port_naming[7]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])
VNA_TEMP_CONCAT.save_2_ports(VNA_P5_BEFORE,_port_naming[8]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P5_AFTER,_port_naming[8]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])
VNA_TEMP_CONCAT.save_2_ports(VNA_P6_BEFORE,_port_naming[9]+' '+_legend_list[1], _type_of_plot[0], _s_param_list[2],VNA_P6_AFTER,_port_naming[9]+' '+_legend_list[3], _type_of_plot[0], _s_param_list[2])


#VNA_P3_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P4_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
#VNA_P5_BEFORE.save(_legend_list[0], _type_of_plot[0], _s_param_list[0])
