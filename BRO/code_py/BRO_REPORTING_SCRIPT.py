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

'''
Class Object Initialisation
'''
VNA_1       =   vna.VNA()
VNA_2       =   vna.VNA()
VNA_3       =   vna.VNA()
VNA_4       =   vna.VNA()
VNA_TEMP    =   vna.VNA()

warehouse_file_name =   'H:\DATA_WARE_HOUSE\VNA_set_1.pkl'

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
list_of_objects.append(VNA_TEMP)

print('ADRESS:', VNA_TEMP.S2P)
VNA_TEMP.WorkingDirectory = 'H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'

VNA_TEMP.save('BRO_9_S_BAND_LNA',"angle_unwrapped",'S11')
VNA_TEMP.save('BRO_9_S_BAND_LNA',"magnitude_dB",'S11')
VNA_TEMP.save('BRO_9_S_BAND_LNA',"angle_with_rotations",'S11')
## To be debugged - something wrong with Save function
# VNA_TEMP.save('BRO_9_S_BAND_LNA',"smith",'S11')

##VNA_TEMP.__save_S22('BRO_9_S_BAND_LNA',"angle_unwrapped")
##VNA_TEMP.__save_S21('BRO_9_S_BAND_LNA',"angle_unwrapped")
##VNA_TEMP.__save_S12('BRO_9_S_BAND_LNA',"angle_unwrapped")
