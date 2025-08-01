"""
Main Script as per BRO S_Band Check_Out:
4 sets of 4 LNB to be verified:
S_BAND_LNB
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

## If _LNB_number = 0 then it is calibration kit

_file_name_for_saving_S2P   =   ''
_file_name_for_saving_SC    =   ''

pdiv        = 10
ref         = 0
V_bw        = 0
R_bw        = 30
avg         = 10
Stop_freq   = 15000
Start_freq  = 2000
C_freq      = 5000
points      = 801
offset      = -50
_lim        =   0
_data       =   []

### references given on the package from production
_LNB_number = 4
_LNB_serial_number = 1
_Branche_number = 4
_str_IP_vector_analyzer = "10.0.8.112"

if (_LNB_number == 0):
    object_name = 'cal_kit'
else:
    object_name = 'LNB'+str(_LNB_number)

serial_nmuber = 'ZV-135'
#object_name = 'LNB1'

warehouse_directory = 'H:\\DATA_WARE_HOUSE'
if not os.path.exists(warehouse_directory):
    os.makedirs(warehouse_directory)

warehouse_sub_directory = warehouse_directory + '\\data'
if not os.path.exists(warehouse_sub_directory):
    os.makedirs(warehouse_sub_directory)

if (_LNB_number == 0):
    warehouse_sub_directory = warehouse_directory + '\\data\\CAL'
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)
else:
    warehouse_sub_directory = warehouse_directory + '\\data\\LNB'+str(_LNB_number)+'\\'+'SN'+str(_LNB_serial_number)
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)


warehouse_file_name = warehouse_sub_directory + '\\' + object_name +'.pkl'

warehouse_file_name_target      =   warehouse_file_name
_file_name_Spurious             =   ''


_date_manufacturing_creation    =   '2025-01-13'
_data_check_out_test            =   '2025-01-13'
_Adr_LNB                        = ['0x48','0x49','0x4A','0x4B' ]
# for test
#_Adr_LNB                        = [0x4C,0x4C,0x4C,0x4C]

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
VNA_1.adress_hexadecimal    = _LNB_number
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


if (_LNB_number == 0):
    if not os.path.exists('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+'SN'+str(_LNB_serial_number)):
        os.makedirs('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+'SN'+str(_LNB_serial_number))
else:
    if not os.path.exists('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\LNB'+str(_LNB_number)+'\\'+'SN'+str(_LNB_serial_number)):
        os.makedirs('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\LNB'+str(_LNB_number)+'\\'+'SN'+str(_LNB_serial_number))

## status 20/12 removing the adress verification
##if (_LNB_number > 0):
Status, VNA_1.temperature_check_out,  _port, _inuse, VNA_1.serial_number                    =      LNA.LNA_Identification(_LNB_number)

#Status, _file_name_for_saving_SC, _file_name_for_saving_S2P,_data                               =      GAIN._S_BAND_SPARAMETER(_LNB_number, _LNB_serial_number, _str_IP_vector_analyzer)

### Temporary

#_NF_passed_status,_file_name_NF                                                            =      NF._NOISE_FIGURE_MEASURMENTS(0, 0, 0, 0, 0, 0, 0, _LNB_number, _LNB_serial_number)

#_NF_passed_status,_file_name_NF = NF._NOISE_FIGURE_MEASURMENTS_X_BAND2()

#_SPURIOUS_passed_status, _file_name_Spurious                                               =      SP._SPURIOUS_MEASURMENTS_X_BAND(pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset,_lim, _LNB_number, _Branche_number, '10.0.9.212')
VNA_1.Spurious              = _file_name_Spurious
VNA_1.adress_hexadecimal    = _Adr_LNB[_LNB_number-1]
VNA_1.S2P                   = _file_name_for_saving_S2P
VNA_1.Gain_SC               = _file_name_for_saving_SC # GAIN UP TO SCREENSHOT
VNA_1.Gain                  = _data

with open(warehouse_file_name_target, 'wb') as outp:
    pickle.dump(VNA_1, outp, pickle.HIGHEST_PROTOCOL)
outp.close()
print('Target Object saved')

print('Ready for reporting')
