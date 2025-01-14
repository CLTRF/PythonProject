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
Phase_Reference =   3

LNB_1 = ['LNA1_090125_161728Gain.S2P', 'LNA1_090125_162022Gain.S2P', 'LNA1_090125_162415Gain.S2P', 'LNA1_090125_162708Gain.S2P']
LNB_2 = ['LNA1_100125_103922Gain.S2P', 'LNA1_100125_104912Gain.S2P', 'LNA1_100125_104403Gain.S2P', 'LNA1_100125_105036Gain.S2P']
LNB_3 = ['LNA1_100125_143223Gain.S2P', 'LNA1_100125_142554Gain.S2P', 'LNA1_100125_142732Gain.S2P', 'LNA1_100125_142913Gain.S2P']
LNB_4 = ['LNA1_100125_110815Gain.S2P', 'LNA1_100125_110939Gain.S2P', 'LNA1_100125_111120Gain.S2P', 'LNA1_100125_111409Gain.S2P']
LNB_LIST = []
LNB_LIST.append(LNB_1)
LNB_LIST.append(LNB_2)
LNB_LIST.append(LNB_3)
LNB_LIST.append(LNB_4)

### Provision to Excel Generation file

#filename = 'output//' + filename + '.xlsx'
#if os.path.isfile(filename):
#    workbook = load_workbook(filename)
#else:
#    workbook = Workbook()

_LNB_number                 = 2
_Branche_number             = 1


if (_LNB_number == 0):
    object_name = 'cal_kit'
else:
    object_name = 'LNB'+str(_LNB_number)

warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name_LNB(_LNB_number, _Branche_number)
print('loading object from:', warehouse_file_name)
VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)


VNA_TEMP_CONCAT = VNA_TEMP

_file_length = 26
_file_name_S2P = VNA_TEMP.S2P[:-_file_length]
_reconstructed =  _file_name_S2P + LNB_LIST[_LNB_number-1][_Branche_number-1]
# _device = Network(self.S2P)
VNA_TEMP.change_name(_reconstructed)

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
_BASIC_PROCESSING = False

if (_BASIC_PROCESSING == True):

    __S_PARAMETER_DISPLAY       =   'S_PARAM'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S22'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S21'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_' +__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S11'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    #VNA_TEMP.save('object_name+'_'+str(_LNA_serial_number)+'_''+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY)
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    sleep(1)

    __S_PARAMETER_DISPLAY       =   'S12'
    VNA_TEMP.WorkingDirectory   =   warehouse_sub_directory + '\\' + __S_PARAMETER_DISPLAY
    #VNA_TEMP.save(object_name+'_'+str(_LNA_serial_number)+'_'+__S_PARAMETER_DISPLAY,"smith",__S_PARAMETER_DISPLAY)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"angle_unwrapped",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"magnitude_dB",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    VNA_TEMP.save_LNB(object_name+'_'+str(_LNB_number)+'_'+__S_PARAMETER_DISPLAY,"angle_with_rotations",__S_PARAMETER_DISPLAY, warehouse_sub_directory)
    sleep(1)
else:
    for _LNB_number in range(1,5,1):
        _Branche_number = 1

        list_of_objects = []
        UW_Phase_Table = []

        warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name_LNB(_LNB_number, _Branche_number)
        print('loading object from:', warehouse_file_name)
        VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
        _file_length = 26
        _file_name_S2P = VNA_TEMP.S2P[:-_file_length]
        _reconstructed = warehouse_sub_directory + LNB_LIST[_LNB_number - 1][_Branche_number - 1]
        VNA_TEMP.change_name(_reconstructed)
        print('ADRESS:', VNA_TEMP.S2P)
        VNA_TEMP.change_name(_reconstructed)
        list_of_objects.append(VNA_TEMP)
        _Branche_number += 1

        warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name_LNB(_LNB_number, _Branche_number)
        print('loading object from:', warehouse_file_name)
        VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
        _file_length = 26
        _file_name_S2P = VNA_TEMP.S2P[:-_file_length]
        _reconstructed = warehouse_sub_directory + LNB_LIST[_LNB_number - 1][_Branche_number - 1]
        VNA_TEMP.change_name(_reconstructed)
        print('ADRESS:', VNA_TEMP.S2P)
        VNA_TEMP.change_name(_reconstructed)
        list_of_objects.append(VNA_TEMP)
        _Branche_number += 1

        warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name_LNB(_LNB_number, _Branche_number)
        print('loading object from:', warehouse_file_name)
        VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
        _file_length = 26
        _file_name_S2P = VNA_TEMP.S2P[:-_file_length]
        _reconstructed = warehouse_sub_directory + LNB_LIST[_LNB_number - 1][_Branche_number - 1]
        VNA_TEMP.change_name(_reconstructed)
        print('ADRESS:', VNA_TEMP.S2P)
        VNA_TEMP.change_name(_reconstructed)
        list_of_objects.append(VNA_TEMP)
        _Branche_number += 1

        warehouse_file_name, warehouse_sub_directory = GAIN.build_file_name_LNB(_LNB_number, _Branche_number)
        print('loading object from:', warehouse_file_name)
        VNA_TEMP = GAIN.read_pkl_object(warehouse_file_name)
        _file_length = 26
        _file_name_S2P = VNA_TEMP.S2P[:-_file_length]
        _reconstructed = warehouse_sub_directory + LNB_LIST[_LNB_number - 1][_Branche_number - 1]
        VNA_TEMP.change_name(_reconstructed)
        print('ADRESS:', VNA_TEMP.S2P)
        VNA_TEMP.change_name(_reconstructed)
        list_of_objects.append(VNA_TEMP)
        _Branche_number += 1


        a1 = str(1)
        a2 = str(2)
        a3 = str(3)
        a4 = str(4)

        __S_PARAMETER_DISPLAY       =   'All_Phase_United'
        VNA_TEMP.WorkingDirectory   =   'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+__S_PARAMETER_DISPLAY

                    ##__S_PARAMETER_DISPLAY       =   'All_Phase_United'+'\\'+'SN'+a1+'\\'+'SN'+a2+'\\'+'SN'+a3+'\\'+'SN'+a4
                    ##VNA_TEMP.WorkingDirectory   =   'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+__S_PARAMETER_DISPLAY

        if not os.path.exists(VNA_TEMP.WorkingDirectory):
            os.makedirs(VNA_TEMP.WorkingDirectory)
    # Need a debug

        [UW_Phase_LNB_1, UW_Phase_LNB_2, UW_Phase_LNB_3, UW_Phase_LNB_4, Frequency_Vector] = VNA_TEMP_CONCAT.concat(list_of_objects[0], list_of_objects[1],list_of_objects[2],list_of_objects[3],"angle_unwrapped")
        #[UW_Phase_LNB_1, UW_Phase_LNB_2, UW_Phase_LNB_3, UW_Phase_LNB_4,Frequency_Vector] = VNA_TEMP_CONCAT.concat_gain(list_of_objects[0], list_of_objects[1],list_of_objects[2], list_of_objects[3], "gain")
#
        #UW_Phase_Table.append(UW_Phase_LNB_1)
        #UW_Phase_Table.append(UW_Phase_LNB_2)
        #UW_Phase_Table.append(UW_Phase_LNB_3)
        #UW_Phase_Table.append(UW_Phase_LNB_4)

#                    Item_name_1 = "LNA"+str(_LNA_number_1) + "_"+ "SN"+ str(_LNA_serial_number_1)
#                    Item_name_2 = "LNA"+str(_LNA_number_2) + "_"+ "SN"+ str(_LNA_serial_number_2)
#                    Item_name_3 = "LNA"+str(_LNA_number_3) + "_"+ "SN"+ str(_LNA_serial_number_3)
#                    Item_name_4 = "LNA"+str(_LNA_number_4) + "_"+ "SN"+ str(_LNA_serial_number_4)
                    ##Status = GAIN.Plot_and_Save_Delta_Phase(Frequency_Vector, UW_Phase_Table, Phase_Reference, VNA_TEMP.WorkingDirectory+'\\Phase_Diff_deg',Item_name_1,Item_name_2,Item_name_3,Item_name_4,+10, -10)
                    #Status = GAIN.Plot_and_Save_Magnitude_Phase(Frequency_Vector, UW_Phase_Table, VNA_TEMP.WorkingDirectory+'\\PhaseMag\\'+'\\Phase_Magnitude_deg',Item_name_1,Item_name_2,Item_name_3,Item_name_4 )


                    ### Gain comparison

        index_start_freq    =   840
        index_stop_freq     =   950

        UW_Phase_Table.append(UW_Phase_LNB_1[index_start_freq:index_stop_freq])
        UW_Phase_Table.append(UW_Phase_LNB_2[index_start_freq:index_stop_freq])
        UW_Phase_Table.append(UW_Phase_LNB_3[index_start_freq:index_stop_freq])
        UW_Phase_Table.append(UW_Phase_LNB_4[index_start_freq:index_stop_freq])
        Frequency_Vector_plot   =   Frequency_Vector[index_start_freq:index_stop_freq]
        #Frequency_Vector_plot = Frequency_Vector

        Item_name_1 = "LNB" + str(_LNB_number) + "_" + "BRANCHE" + str(1)
        Item_name_2 = "LNB" + str(_LNB_number) + "_" + "BRANCHE" + str(2)
        Item_name_3 = "LNB" + str(_LNB_number) + "_" + "BRANCHE" + str(3)
        Item_name_4 = "LNB" + str(_LNB_number) + "_" + "BRANCHE" + str(4)

        Status = GAIN.Plot_and_Save_Delta_Phase(Frequency_Vector_plot, UW_Phase_Table, Phase_Reference,VNA_TEMP.WorkingDirectory + '\\Phase_Diff_deg', Item_name_1,Item_name_2, Item_name_3, Item_name_4, +10, -10,'Branche')

        #Status = GAIN.Plot_and_Save_Magnitude_Phase(Frequency_Vector_plot, UW_Phase_Table,VNA_TEMP.WorkingDirectory + '\\Phase_Magnitude_deg',Item_name_1, Item_name_2, Item_name_3, Item_name_4)
#
        #Status = GAIN.Plot_and_Save_Magnitude_Gain(Frequency_Vector_plot, UW_Phase_Table,VNA_TEMP.WorkingDirectory + '\\Gain_Magnitude_dB',Item_name_1, Item_name_2, Item_name_3, Item_name_4)