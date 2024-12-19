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
VNA_1           =   vna.VNA()
VNA_2           =   vna.VNA()
VNA_3           =   vna.VNA()
VNA_4           =   vna.VNA()
VNA_TEMP        =   vna.VNA()
VNA_TEMP_CONCAT =   vna.VNA()
UW_Phase_Table  =   []
Phase_Reference =   0


### Provision to Excel Generation file

#filename = 'output//' + filename + '.xlsx'
#if os.path.isfile(filename):
#    workbook = load_workbook(filename)
#else:
#    workbook = Workbook()

_LNA_number             = 1
_LNA_serial_number      = 93

'''

warehouse_directory             =   'H:\\DATA_WARE_HOUSE'
if not os.path.exists(warehouse_directory):
    os.makedirs(warehouse_directory)

warehouse_sub_directory             =   warehouse_directory+'\\data'
if not os.path.exists(warehouse_sub_directory):
    os.makedirs(warehouse_sub_directory)

if (_LNA_number == 0):
    warehouse_sub_directory = warehouse_directory + '\\data\\CAL'
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)
else:
    #warehouse_sub_directory = warehouse_directory + '\\data\\LNA'+str(_LNA_number)
    warehouse_sub_directory = warehouse_directory + '\\data\\LNA'+str(_LNA_number)+'\\'+'SN'+str(_LNA_serial_number)
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)


warehouse_file_name            =    warehouse_sub_directory +  '\\' + object_name + '.pkl'
#warehouse_file_name             =   'H:\DATA_WARE_HOUSE\VNA_calibration.pkl'

'''

if (_LNA_number == 0):
    object_name = 'cal_kit'
else:
    object_name = 'LNA'+str(_LNA_number)

warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name(_LNA_number, _LNA_serial_number)
print('loading object from:', warehouse_file_name)
quick_fix_name = warehouse_sub_directory+"\\LNA"+str(_LNA_number)+"_S2P.s2p"
VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name, quick_fix_name)


VNA_TEMP_CONCAT = VNA_TEMP
print('ADRESS:', VNA_TEMP.S2P)

if not os.path.exists('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'):
    os.makedirs('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\')
'''
Convention 
P1: INPUT
P2: OUTPUT
S21 = GAIN
'''
_BASIC_PROCESSING = True

if (_BASIC_PROCESSING == True):

    __S_PARAMETER_DISPLAY       =   'S_PARAM'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S22'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S21'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_' +__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S11'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S12'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    sleep(1)
else:
    for _LNA_level_1 in range(0,2,1):
        for _LNA_level_2 in range(0,4,1):
            for _LNA_level_3 in range(0,4):
                for _LNA_level_4 in range(0,4):

                    list_of_objects = []
                    UW_Phase_Table = []

                    _LNA_number_1           =   1
                    _LNA_serial_number_1    =   93+_LNA_level_1
                    _LNA_number_2           =   2
                    _LNA_serial_number_2    =   97+_LNA_level_2
                    _LNA_number_3           =   3
                    _LNA_serial_number_3    =   101+_LNA_level_3
                    _LNA_number_4           =   4
                    _LNA_serial_number_4    =   105+_LNA_level_4

                    warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name(_LNA_number_1, _LNA_serial_number_1)
                    print('loading object from:', warehouse_file_name)
                    VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
                    list_of_objects.append(VNA_TEMP)

                    warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name(_LNA_number_2, _LNA_serial_number_2)
                    print('loading object from:', warehouse_file_name)
                    VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
                    list_of_objects.append(VNA_TEMP)

                    warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name(_LNA_number_3, _LNA_serial_number_3)
                    print('loading object from:', warehouse_file_name)
                    VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
                    list_of_objects.append(VNA_TEMP)

                    warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name(_LNA_number_4, _LNA_serial_number_4)
                    print('loading object from:', warehouse_file_name)
                    VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
                    list_of_objects.append(VNA_TEMP)

                    __S_PARAMETER_DISPLAY       =   'All_Phase_United'
                    VNA_TEMP.WorkingDirectory   =   'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+__S_PARAMETER_DISPLAY
    # Need a debug

                    [UW_Phase_LNA_1, UW_Phase_LNA_2, UW_Phase_LNA_3, UW_Phase_LNA_4, Frequency_Vector] = VNA_TEMP_CONCAT.concat(list_of_objects[0], list_of_objects[1],list_of_objects[2],list_of_objects[3],"angle_unwrapped")
#                    [UW_Phase_LNA_1, UW_Phase_LNA_2, UW_Phase_LNA_3, UW_Phase_LNA_4,
#                     Frequency_Vector] = VNA_TEMP_CONCAT.concat_gain(list_of_objects[0], list_of_objects[1],
#                                                                     list_of_objects[2], list_of_objects[3], "gain")

                    UW_Phase_Table.append(UW_Phase_LNA_1)
                    UW_Phase_Table.append(UW_Phase_LNA_2)
                    UW_Phase_Table.append(UW_Phase_LNA_3)
                    UW_Phase_Table.append(UW_Phase_LNA_4)

                    Item_name_1 = "LNA"+str(_LNA_number_1) + "_"+ "SN"+ str(_LNA_serial_number_1)
                    Item_name_2 = "LNA"+str(_LNA_number_2) + "_"+ "SN"+ str(_LNA_serial_number_2)
                    Item_name_3 = "LNA"+str(_LNA_number_3) + "_"+ "SN"+ str(_LNA_serial_number_3)
                    Item_name_4 = "LNA"+str(_LNA_number_4) + "_"+ "SN"+ str(_LNA_serial_number_4)
                    Status = GAIN.Plot_and_Save_Delta_Phase(Frequency_Vector, UW_Phase_Table, Phase_Reference, VNA_TEMP.WorkingDirectory+'\\Phase_Diff_deg',Item_name_1,Item_name_2,Item_name_3,Item_name_4,+10, -10)
                    Status = GAIN.Plot_and_Save_Magnitude_Phase(Frequency_Vector, UW_Phase_Table, VNA_TEMP.WorkingDirectory+'\\PhaseMag\\'+'\\Phase_Magnitude_deg',Item_name_1,Item_name_2,Item_name_3,Item_name_4 )


                    ### Gain comparison


                    #UW_Phase_Table.append(UW_Phase_LNA_1)
                    #UW_Phase_Table.append(UW_Phase_LNA_2)
                    #UW_Phase_Table.append(UW_Phase_LNA_3)
                    #UW_Phase_Table.append(UW_Phase_LNA_4)

                    #Item_name_1 = "LNA" + str(_LNA_number_1) + "_" + "SN" + str(_LNA_serial_number_1)
                    #Item_name_2 = "LNA" + str(_LNA_number_2) + "_" + "SN" + str(_LNA_serial_number_2)
                    #Item_name_3 = "LNA" + str(_LNA_number_3) + "_" + "SN" + str(_LNA_serial_number_3)
                    #Item_name_4 = "LNA" + str(_LNA_number_4) + "_" + "SN" + str(_LNA_serial_number_4)
                    #Status = GAIN.Plot_and_Save_Delta_Gain(Frequency_Vector, UW_Phase_Table, Phase_Reference,
                    #                                        VNA_TEMP.WorkingDirectory + '\\Gain_Diff_deg', Item_name_1,
                    #                                        Item_name_2, Item_name_3, Item_name_4, +10, -10)
                    #Status = GAIN.Plot_and_Save_Magnitude_Phase(Frequency_Vector, UW_Phase_Table,
                    #                                            VNA_TEMP.WorkingDirectory + '\\Phase_Magnitude_deg',
                    #                                            Item_name_1, Item_name_2, Item_name_3, Item_name_4)

