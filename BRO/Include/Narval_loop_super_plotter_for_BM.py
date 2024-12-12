import sys
sys.path.insert(0,'C:\\Users\\CALAU\\GitHUB\\MK0_POSTPROCESSING\\PycharmProjects\\includes')
import sensors_construction
from datetime import datetime
import misc
import numpy as np
import pickle
import os
import sensors_construction
from patterns import Sensors

#import includes.data_load_store
#sensors_construction.init_global()

''' Class with the structure of the DATA '''

#Initalize statics
## CODE VERSION TO BE USED FOR SIT3 REPORTING
## REMEMBER: FOR ZF GEARBOX !!! ONLY 2 POSITIONS
Path_to_folder = "C:/Users/CALAU/OneDrive - Vestas Wind Systems A S/Documents/DataFromLecroy"
Path_for_figures = 'C:/Users/CALAU/OneDrive - Vestas Wind Systems A S/Documents/DataFromLecroy/DMS_0100-7636/output'

##CHANNEL_TO_MANIPULATE_WTG = 4?

C1_RC_PROBE_POL_1   = Sensors()
C2_RC_PROBE_POL_2   = Sensors()
C3_FLASH_ANTENNA    = Sensors()

Channel_number = 0
Speed_rotation_rpm  = 100
Power_kW            = 500
Type_of_power       = 'P'
notching_selector_LORC   = False
notching_selector_WTG    = False
Gain_detector       = 187
type_of_sub_plot    = ' '
band_to_analyze     = ' '

# Parametrization CISPR
#Start_Bd_A_Freq_Hz = 1200
#Stop_Bd_A_Freq_Hz  = 1500000
#Start_Bd_B_Freq_Hz = 1500000
#Stop_Bd_B_Freq_Hz  = 3000000
#RBW_A_Hz           = 30
#RBW_B_Hz           = 90000

# Parametrization CISPR
#Start_Bd_A_Freq_Hz = 10
#Stop_Bd_A_Freq_Hz  = 20
#Start_Bd_B_Freq_Hz = 10
#Stop_Bd_B_Freq_Hz  = 60000000
#RBW_A_Hz           = 5000
#RBW_B_Hz           = 4000

# Parametrization CISPR
Start_Bd_A_Freq_Hz = 90
Stop_Bd_A_Freq_Hz  = 150000
Start_Bd_B_Freq_Hz = 150000
Stop_Bd_B_Freq_Hz  = 3000000
RBW_A_Hz           = 20
RBW_B_Hz           = 9000

FFT_Averaging_selector  =   False

# Parametrization AVERAGING
# 200 for Band A ## 500 for Band B
Averaging_Time        = 200
PHASE_TO_MANIPULATE = '_'

save = True
split_plots = False
block_display = True

band_list_for_freq_Analysis = ['B1','B2', 'B3', 'B4', 'Full_CISPR16']

#data_c_POS_2 = lecroyparser.ScopeData(Path, parseAll=True)

# Initialize an object from the class
# from DVPR document

Speed_rotation_rpm = 'NA'

start_test_point = 1
stop_test_point = 14
step_scan = 1
################# LORC with ZF GearBox

warehouse_file_name = 'D:/tmp/a-directory/sensor_class_Idle_extended_TC#0_to_TC#21_correction_ExtraC10C110p1_Part2_TC1_to_TC21_fullset.pkl'
warehouse_file_name = 'D:/tmp/a-directory/sensor_class_TC0_to_TC21_dVdt500_full_CSIPR16_fft_VCM_CORBUG.pkl'
warehouse_file_name = 'D:/tmp/a-directory/sensor_class_TC0_to_TC21_dVdt500_full_CSIPR16_fft_VCM_CORBUG_MBA_ADDON_FILT_NRE_NOTCH_2455Hz.pkl'
warehouse_file_name = 'D:/tmp/a-directory/sensor_class_TC0_to_TC21_dVdt500_full_CSIPR16_fft_VCM_CORBUG.pkl'

print('loading object from:', warehouse_file_name)

with open(warehouse_file_name, 'rb') as input:
    number_of_objects_to_be_loaded = pickle.load(input)
    list_of_objects = []
    #number_of_objects_to_be_loaded = 53
    #number_of_objects_to_be_loaded = 1

    for i in range(0,number_of_objects_to_be_loaded,1):
        Sensor_1_GENERIC = pickle.load(input)
        print('i:',i)
        list_of_objects.append(Sensor_1_GENERIC)

input.close()
print('log: object loaded')

#C_GEAR.compute_peak_fft_cispr(Start_Bd_A_Freq_Hz, Stop_Bd_A_Freq_Hz, Start_Bd_B_Freq_Hz,Stop_Bd_B_Freq_Hz, RBW_A_Hz, RBW_B_Hz, Averaging_Time, FFT_Averaging_selector)

C_GROUP_TO_PLOT         = Sensors()

Temp_multiply_Object                = Sensors()
Temp_multiply_Object.set_s_struct(0, 0, '8MW', 'ESBJERG', 'ESD dectector', 'ESD dectector', 'ESD dectector', 'ESD dectector', 'NA', '', '', '', datetime.now(), 'NA', 'ON')
#Temp_multiply_Object.multiply(list_of_objects[3],Gain_detector)


fft_recalculate = False
#type_of_plot = 'PeakFFT'
#type_of_plot = 'AvgFFT'
#type_of_plot = 'vi'
#type_of_plot = "dVdt"

# For U,V,W Group1 Left winding
#sensor_number_to_plot   =   [10,12,14]

# for U Gr1, Gr2 left winding
#sensor_number_to_plot   =   [10]

# for U Gr1, Gr2 left winding
##33,34 are empty?
sensor_number_to_plot   =   [10,11,12,13,14,15]
index_TC = [7,8,15, 16, 17, 18, 19, 20]
indicator_acquisition2 = True
index_list_1 = []

index_test_case = []
number_of_sensors = len(sensor_number_to_plot)
number_of_test_case = 0


for i in range(0, len(index_TC), 1):
    index_test_case.append(index_TC[i]*2)
    if ( indicator_acquisition2 == True):
        index_test_case.append(index_TC[i] * 2 + 1)

if (type_of_plot == 'dVdt'):
    print('dVdt calculation')
    list_of_objects[sensor_number_to_plot].compute_dVdT(True)
if (type_of_plot == 'PeakFFT') and (fft_recalculate == True):
    list_of_objects[sensor_number_to_plot].compute_peak_fft_cispr(Start_Bd_A_Freq_Hz, Stop_Bd_A_Freq_Hz, Start_Bd_B_Freq_Hz,
                                            Stop_Bd_B_Freq_Hz, RBW_A_Hz, RBW_B_Hz, Averaging_Time,
                                            FFT_Averaging_selector, band_list_for_freq_Analysis[4])

for i in range(0, number_of_sensors, 1):
    C_GROUP_TO_PLOT.vi.append(list_of_objects[sensor_number_to_plot[i]].vi)
    index_list_1.append(i)
#C_GROUP_TO_PLOT.vi.append(list_of_objects[26].vi)
#C_GROUP_TO_PLOT.vi.append(list_of_objects[2].vi)
#C_GROUP_TO_PLOT.vi.append(list_of_objects[3].vi)
#C_GROUP_TO_PLOT.vi.append(Temp_multiply_Object.vi)



if ( type_of_plot == 'PeakFFT'):
    lin_log_x = 'log'
    lin_log_y = 'log_dB'
    type_of_sub_plot = 'fft_fFull_CISPR16'
    band_to_analyze = 'Full_CISPR16'
    type_of_sub_plot = band_to_analyze
    #band_to_analyze = 'B1'

if (type_of_plot == 'vi'):
    lin_log_x = 'lin'
    lin_log_y = 'lin'

if (type_of_plot == 'dVdt'):
    lin_log_x = 'lin'
    lin_log_y = 'lin'


#C_GROUP_TO_PLOT.vi.append(V17_Vu1_g_GEN_Machine_GENERIC.vi)

#C_GROUP_TO_PLOT.vi.append(C23_converter_pow_to_gen1_GENERIC.vi)
Plot_info_str = 'GearAndBrush'

    ## index_list_2: Children list and in the corresponding parent looking for children
    ### 0 , 1, 2: NA 3: 500 kW 4: 5750 kW

    ## 4 50 kW Q-Production
    ## 5 5750 kW P-Production

### Looping on test case ###
#### concatenate = False
####  for i in range(0,stop_test_point-start_test_point,1):

### result agregation
###concatenate_result = True
###if (concatenate_result == True):

### Looping on sensors

for i in range(0, number_of_sensors,1):

    #index_list_1 = [0, 1, 3]
## One used for the title
    # index_list_stash = [i]
    ## substract 1 to TCnumber
    index_list_stash = index_test_case
    index_title = 0
    #index_list_stash = [ 0, 9]
    index_list_2 = index_list_stash.copy()
    index_list_3 = index_list_stash.copy()
    vector_add_up = np.ones(len(index_list_stash))*number_of_test_case
    Parent = 0
    if (Parent == 0):
        Path_Ext = str(C_GROUP_TO_PLOT.vi[Parent][Parent]['location'])
        Children = i

    if (Parent == 1):
        Path_Ext = str(C_GROUP_TO_PLOT.vi[Parent][Parent+number_of_test_case]['location'])
        Children = i + number_of_test_case
        start_2 = 0
        j= 0
        for j, start_2 in enumerate(index_list_stash):
            index_list_2[j] = index_list_stash[j]+number_of_test_case

    if (Parent == 2):
        Path_Ext = str(C_GROUP_TO_PLOT.vi[Parent][Parent]['location'])+'_'+str(C_GROUP_TO_PLOT.vi[Parent][Parent+number_of_test_case]['location'])
        Children = i
        start_2 = 0
        j = 0
        for j, start_2 in enumerate(index_list_stash):
            index_list_3[j] = index_list_stash[j]+number_of_test_case
        index_list_2 = index_list_2 + index_list_3

    #Basic_title = "Pitch circuit in "+ Path_Ext
    Basic_title = ''
    lower_limit_s_Hz = -50
    upper_limit_s_Hz = +50
    title = 'V17_u'+ ' ' + Basic_title

    title, date, unit_x, unit_y = C_GROUP_TO_PLOT.create_a_plot_title(Basic_title, type_of_plot, index_list_1, index_title, Parent, Children)

    C_GROUP_PLOT_PATTERN = Sensors()
    C_GROUP_PLOT_PATTERN = C_GROUP_TO_PLOT.create_list_of_plots(type_of_plot, type_of_sub_plot, index_list_1,index_list_2, lower_limit_s_Hz, upper_limit_s_Hz)
    C_LEGEND_TO_WRITE    = C_GROUP_TO_PLOT.create_legend_to_plot(index_list_1,index_list_2,'location', 'power_kW')

    PHASE_TO_MANIPULATE = '_'
    number_str_1 = title
    number_str_2 = 'Generator'
    Current_STR = str(i)
    Overall_path = Path_for_figures + '/' + Path_Ext + '/'
    if not os.path.exists(Overall_path):
        os.makedirs(Overall_path)

    String_text_for_figure = number_str_1 + '-' + number_str_2 + '_' + Current_STR
    Parent_filter = Path_Ext
#    fig_number = C_GROUP_PLOT_PATTERN.plot_and_save(title, type_of_plot, unit_x, unit_y, lin_log_x, lin_log_y, C_LEGEND_TO_WRITE, save, split_plots, block_display, Overall_path, PHASE_TO_MANIPULATE, Current_STR+'_'+Parent_filter+Plot_info_str)
    fig_number = C_GROUP_PLOT_PATTERN.plot_and_save(title, type_of_plot, unit_x, unit_y, lin_log_x, lin_log_y, C_LEGEND_TO_WRITE, save, split_plots, block_display, Overall_path, PHASE_TO_MANIPULATE, title, date, band_to_analyze)
