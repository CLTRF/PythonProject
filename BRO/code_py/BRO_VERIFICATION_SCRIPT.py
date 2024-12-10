"""
Main Script as per BRO S_Band Check_Out:
4 sets of 4 LNA to be verified:
S_BAND_LNA
    4xNoise_Figure
    4xSpurious

X_BAND_RECEIVER
    4xS_PARAMETERS: Magnitude and Unwrapped Phase
    4x
"""

import sys, os

from pyvisa.constants import VI_ERROR_BERR, VI_ATTR_WIN_BASE_ADDR_32, VI_ATTR_WIN_BASE_ADDR_64

sys.path.insert(1, 'C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include')
import time
import pickle
### comming from Pickles module
import lna_aadetect as aa_function
import S_BAND_Identification as LNA
import NF_SBAND as NF
import SPURIOUS_SBAND as SP
import class_VNA as vna
from datetime import datetime

_LNA_number_1 = 2

pdiv        = 10
ref         = 0
V_bw        = 0
R_bw        = 30
avg         = 10
Stop_freq   = 15000
Start_freq  = 2000
C_freq      = 5000
points      = 801
offset      = 0
_lim        = 0

warehouse_file_name_target      =   'H:\DATA_WARE_HOUSE\VNA_set_1.pkl'

_date_manufacturing_creation    =   '2018-12-11'
_data_check_out_test            =   '2024-12-09'

'''
Class Object Initialisation
'''
VNA_1   =   vna.VNA()
VNA_2   =   vna.VNA()
VNA_3   =   vna.VNA()
VNA_4   =   vna.VNA()
'''
VNA manufacturing and testing attributes
'''

## VNA1
## To be implemented in loop
VNA_1.adress_hexadecimal    = _LNA_number_1
VNA_1.create_date           = _date_manufacturing_creation
VNA_1.check_out_date        = _data_check_out_test
VNA_1.NF = []
VNA_1.Spurious = []
VNA_1.Gain = []
VNA_1.Phase = []
VNA_1.NF = []
VNA_1.Spurious = []
VNA_1.Gain = []
VNA_1.Phase = []

Status, VNA_1.temperature_check_out,  _port, _inuse, VNA_1.serial_number            =      LNA.LNA_Identification(_LNA_number_1)

_NF_passed_status,_file_name_NF                                                     =      NF._NOISE_FIGURE_MEASURMENTS(0, 0, 0, 0, 0, 0, 0, _LNA_number_1 )
_SPURIOUS_passed_status, _file_name_Spurious                             =      SP._SPURIOUS_MEASURMENTS(pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset,_lim, 2)
#_GAIN_passed_status        =   GAIN_S_BAND()
VNA_1.Spurious = _file_name_Spurious

with open(warehouse_file_name_target, 'wb') as outp:
    pickle.dump(VNA_1, outp, pickle.HIGHEST_PROTOCOL)
outp.close()
print('Target Object saved')

### Trial for reading
#print('loading object from:', warehouse_file_name_target)
with open(warehouse_file_name_target, 'rb') as input_1:
    VNA_2 = pickle.load(input_1)

print('object saved and verified at:', warehouse_file_name_target)
print('Ready for reporting')