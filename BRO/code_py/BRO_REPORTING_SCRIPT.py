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

'''
Class Object Initialisation
'''
VNA_1           =   vna.VNA()
VNA_2           =   vna.VNA()
VNA_3           =   vna.VNA()
VNA_4           =   vna.VNA()
VNA_TEMP        =   vna.VNA()
VNA_TEMP_CONCAT =   vna.VNA()
UW_Phase_Table  =   []
Phase_Reference =   1


### Provision to Excel Generation file

#filename = 'output//' + filename + '.xlsx'
#if os.path.isfile(filename):
#    workbook = load_workbook(filename)
#else:
#    workbook = Workbook()


warehouse_file_name         =   'H:\DATA_WARE_HOUSE\VNA_set_1.pkl'
print('loading object from:', warehouse_file_name)

list_of_objects = []
with open(warehouse_file_name, 'rb') as input:
#    number_of_objects_to_be_loaded = pickle.load(input)
#    list_of_objects = []
#    #number_of_objects_to_be_loaded = 53
    number_of_objects_to_be_loaded = 1
    VNA_TEMP = pickle.load(input)

#for i in range(0,number_of_objects_to_be_loaded,1):
#    VNA_TEMP = pickle.load(input)
#    print('i:',i)
## _TEMP is used during the testing process

list_of_objects.append(VNA_TEMP)
list_of_objects.append(VNA_TEMP)
list_of_objects.append(VNA_TEMP)
list_of_objects.append(VNA_TEMP)

VNA_TEMP_CONCAT = VNA_TEMP

print('ADRESS:', VNA_TEMP.S2P)

__S_PARAMETER_DISPLAY       =   'S21'
VNA_TEMP.WorkingDirectory   =   'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+__S_PARAMETER_DISPLAY

VNA_TEMP.save('BRO_9_S_BAND_LNA_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
VNA_TEMP.save('BRO_9_S_BAND_LNA_'+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
VNA_TEMP.save('BRO_9_S_BAND_LNA_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY)
VNA_TEMP.save('BRO_9_S_BAND_LNA_'+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)

__S_PARAMETER_DISPLAY       =   'All_Phase_United'
VNA_TEMP.WorkingDirectory   =   'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+__S_PARAMETER_DISPLAY

# Need a debug
[UW_Phase_LNA_1, UW_Phase_LNA_2, UW_Phase_LNA_3, UW_Phase_LNA_4, Frequency_Vector] = VNA_TEMP_CONCAT.concat(list_of_objects[0], list_of_objects[1],list_of_objects[2],list_of_objects[3],"angle_unwrapped")

UW_Phase_Table.append(UW_Phase_LNA_1)
UW_Phase_Table.append(UW_Phase_LNA_2)
UW_Phase_Table.append(UW_Phase_LNA_3)
UW_Phase_Table.append(UW_Phase_LNA_4)

Status = GAIN.Plot_and_Save_Delta_Phase(Frequency_Vector, UW_Phase_Table, Phase_Reference, VNA_TEMP.WorkingDirectory+'\\Phase_Diff' )
