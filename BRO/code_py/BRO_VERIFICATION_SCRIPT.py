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

## If _LNA_number = 0 then it is calibration kit

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
_LNA_number = 1
_LNA_serial_number = 93
_str_IP_vector_analyzer = "10.0.8.44"

if (_LNA_number == 0):
    object_name = 'cal_kit'
else:
    object_name = 'LNA'+str(_LNA_number)

serial_nmuber = 'ZV-135'
#object_name = 'LNA1'

warehouse_directory = 'H:\\DATA_WARE_HOUSE'
if not os.path.exists(warehouse_directory):
    os.makedirs(warehouse_directory)

warehouse_sub_directory = warehouse_directory + '\\data'
if not os.path.exists(warehouse_sub_directory):
    os.makedirs(warehouse_sub_directory)

if (_LNA_number == 0):
    warehouse_sub_directory = warehouse_directory + '\\data\\CAL'
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)
else:
    warehouse_sub_directory = warehouse_directory + '\\data\\LNA'+str(_LNA_number)+'\\'+'SN'+str(_LNA_serial_number)
    if not os.path.exists(warehouse_sub_directory):
        os.makedirs(warehouse_sub_directory)


warehouse_file_name = warehouse_sub_directory + '\\' + object_name +'.pkl'

warehouse_file_name_target      =   warehouse_file_name
_file_name_Spurious             =   ''


_date_manufacturing_creation    =   '2024-12-16'
_data_check_out_test            =   '2024-12-16'
_Adr_LNA                        = ['0x49','0x4A','0x4B','0x4C' ]
# for test
#_Adr_LNA                        = [0x4C,0x4C,0x4C,0x4C]

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
VNA_1.adress_hexadecimal    = _LNA_number
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

if (_LNA_number == 0):
    if not os.path.exists('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+'SN'+str(_LNA_serial_number)):
        os.makedirs('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\'+'SN'+str(_LNA_serial_number))
else:
    if not os.path.exists('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\LNA'+str(_LNA_number)+'\\'+'SN'+str(_LNA_serial_number)):
        os.makedirs('H:\\DATA_WARE_HOUSE' + '\\' + 'data\\LNA'+str(_LNA_number)+'\\'+'SN'+str(_LNA_serial_number))

#status                                                                                      =      GAIN.save_to_excel()
if (_LNA_number > 0):
    Status, VNA_1.temperature_check_out,  _port, _inuse, VNA_1.serial_number                    =      LNA.LNA_Identification(_LNA_number)

#status, _file_name_for_saving_SC, _file_name_for_saving_S2P,_data                               =      GAIN._S_BAND_SPARAMETER(_LNA_number, _LNA_serial_number, _str_IP_vector_analyzer)
### Temporary

#_NF_passed_status,_file_name_NF                                                            =      NF._NOISE_FIGURE_MEASURMENTS(0, 0, 0, 0, 0, 0, 0, _LNA_number_1 )
_SPURIOUS_passed_status, _file_name_Spurious                                               =      SP._SPURIOUS_MEASURMENTS(pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset,_lim, _LNA_number, _LNA_serial_number)

VNA_1.Spurious              = _file_name_Spurious
VNA_1.adress_hexadecimal    = _Adr_LNA[_LNA_number-1]
VNA_1.S2P                   = _file_name_for_saving_S2P
VNA_1.Gain_SC               = _file_name_for_saving_SC # GAIN UP TO SCREENSHOT
VNA_1.Gain                  = _data

with open(warehouse_file_name_target, 'wb') as outp:
    pickle.dump(VNA_1, outp, pickle.HIGHEST_PROTOCOL)
outp.close()
print('Target Object saved')


### Trial for reading
#print('loading object from:', warehouse_file_name_target)
with open(warehouse_file_name_target, 'rb') as input_1:
    VNA_2 = pickle.load(input_1)
    print('Target Object saved')
    print('ADRESS;', VNA_2.S2P)

print('object saved and verified at:', warehouse_file_name_target)
print('Ready for reporting')