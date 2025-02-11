def _SPURIOUS_MEASURMENTS(pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset,lim,_LNA_number,_serial_number,_str_IP_spectrum_analyzer):

    """
   this function measures Noise Figure of the BRO S-BAND LNA using N9000A Spectrum Analyzer.
   it passes:
   start frequency in MHz
   stop frequency in MHz
   Spectrum Analyzer Intermediate Frequency in MHz
   Number of points in scalar unit
   ENR in dB
    """

    import sys,os

#sys.path.insert(1, '/home/max/python/myimport')
    sys.path.insert(1, 'C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include')

    import csv
    import copy
    import logging
    import time
    from math import inf
    from types import SimpleNamespace
    import numpy as np
    import gs_instrument
    from gs_instrument import spectrum_analyzer

    import numpy as np
    #import SMU200
    import time
    import json
    import datetime
    import select
    from gs_instrument import InstrumentDummy
    from gs_instrument import CsvWriter

## Test Spec


#    _str_freq_MHz   =   2000
#    _stop_freq_MHz  =   3000
#    _IF_BW_MHz      =   2
#    _Nb_Points_Sc   =   40
#    _ENR_dB         =   6
#   _Frequency_Hz           =   1000000000.0 # 1 GHz
#    _Span_Hz                =   25000000.0 #25 MHz
#    _Rbw_Hz                 =   10
#    _Plevel_dB              =   10
#    _Sweep_points           =   1001
#    _Attenuation_dB         =   0

    pdiv = 10
    ref = 0
    V_bw = 0
    R_bw = 30
    avg = 10
    Stop_freq = 15000
    Start_freq = 2000
    C_freq = 5000
    points = 801
    offset = -50
    _lim = -50
    _data = []
    _Detector_Positive_Peak =   True
    _Path_to_screen_shot    =   'F:\\'
    _file_name              =   'LNA1'
    _format_file_screen     =   'PNG'

    _str_freq_MHz   =   Start_freq
    _stop_freq_MHz  =   Stop_freq
    _IF_BW_MHz      =   2
    _Nb_Points_Sc   =   points
    _ENR_dB         =   6
    _Frequency_Hz           =   1000000000.0 # 1 GHz
    _Span_Hz                =   25000000.0 #25 MHz
    _Rbw_Hz                 =   10
    _Plevel_dB              =   10
    _Sweep_points           =   1001
    _Attenuation_dB         =   0


    # local variables Initialisation
    _str_IP_spectrum_analyzer = "10.0.9.212"
    _N9000a=spectrum_analyzer.KeysightCXA(_str_IP_spectrum_analyzer)
    _N9000a.spur_subband_BRO(offset)
    _N9000a.Spurious_BRO(pdiv, ref, V_bw, R_bw, avg, Stop_freq, Start_freq, C_freq, points, offset)

    #_SPURIOUS_passed_status, _file_name_Spurious = Spurious_BRO(self, pdiv, ref, V_bw, R_bw, avg, Stop_freq, Start_freq,
    #                                                            C_freq, points, offset)

    #############################################################

    time.sleep(5)
    _now = datetime.datetime.now()
    _now_string = _now.strftime("%d%m%y_%H%M%S")
    #_now_string_time = _now_time.strftime("%H%M%S")
    #_now_string_date = _now_string_date + _now_string_time

    #_file_name_for_saving = "H:\\DATA_WARE_HOUSE\\data\\"+"LNA"+str(_LNA_number)+"SN"+str(_serial_number)+"\\" + "_now_string_Spurious+Screenshot.png"
    _file_name_for_saving = "F:\\LNA" + str(_LNA_number) + "\\" + _now_string + "\\Spurious\\" + "Screenshot_LNA"+str(_LNA_number)+"_"+str(_serial_number)+".png"
    _N9000a.save_screenshot_png(_file_name_for_saving)

    ## _N9000a.save_screenshot_png('F:/FOU/')

    return(True, _file_name_for_saving)


def _SPURIOUS_MEASURMENTS_X_BAND(pdiv,ref,V_bw,R_bw,avg,Stop_freq,Start_freq,C_freq,points,offset,lim,_LNB_number,_Branche_number,_str_IP_spectrum_analyzer):

    """
   this function measures Noise Figure of the BRO S-BAND LNA using N9000A Spectrum Analyzer.
   it passes:
   start frequency in MHz
   stop frequency in MHz
   Spectrum Analyzer Intermediate Frequency in MHz
   Number of points in scalar unit
   ENR in dB
    """

    import sys,os

#sys.path.insert(1, '/home/max/python/myimport')
    sys.path.insert(1, 'C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include')

    import csv
    import copy
    import logging
    import time
    from math import inf
    from types import SimpleNamespace
    import numpy as np
    import gs_instrument
    from gs_instrument import spectrum_analyzer

    import numpy as np
    #import SMU200
    import time
    import json
    import datetime
    import select
    from gs_instrument import InstrumentDummy
    from gs_instrument import CsvWriter

## Test Spec


#    _str_freq_MHz   =   2000
#    _stop_freq_MHz  =   3000
#    _IF_BW_MHz      =   2
#    _Nb_Points_Sc   =   40
#    _ENR_dB         =   6
#   _Frequency_Hz           =   1000000000.0 # 1 GHz
#    _Span_Hz                =   25000000.0 #25 MHz
#    _Rbw_Hz                 =   10
#    _Plevel_dB              =   10
#    _Sweep_points           =   1001
#    _Attenuation_dB         =   0

    pdiv = 10
    ref = 0
    V_bw = 0
    R_bw = 30
    avg = 10
    Stop_freq = 26000
    Start_freq = 2600
    C_freq = 5000
    points = 801
    offset = -50
    _lim = -50
    _data = []
    _Detector_Positive_Peak =   True
    _Path_to_screen_shot    =   'F:\\'
    _file_name              =   'LNB1'
    _format_file_screen     =   'PNG'

    _str_freq_MHz   =   Start_freq
    _stop_freq_MHz  =   Stop_freq
    _IF_BW_MHz      =   2
    _Nb_Points_Sc   =   points
    _ENR_dB         =   6
    _Frequency_Hz           =   1000000000.0 # 1 GHz
    _Span_Hz                =   25000000.0 #25 MHz
    _Rbw_Hz                 =   10
    _Plevel_dB              =   10
    _Sweep_points           =   1001
    _Attenuation_dB         =   0


    # local variables Initialisation
    _str_IP_spectrum_analyzer = "10.0.9.212"
    _N9000a=spectrum_analyzer.KeysightCXA(_str_IP_spectrum_analyzer)
    _N9000a.spur_subband_BRO(offset)
    _N9000a.Spurious_BRO(pdiv, ref, V_bw, R_bw, avg, Stop_freq, Start_freq, C_freq, points, offset)

    #_SPURIOUS_passed_status, _file_name_Spurious = Spurious_BRO(self, pdiv, ref, V_bw, R_bw, avg, Stop_freq, Start_freq,
    #                                                            C_freq, points, offset)

    #############################################################

    time.sleep(5)
    _now = datetime.datetime.now()
    _now_string = _now.strftime("%d%m%y_%H%M%S")
    #_now_string_time = _now_time.strftime("%H%M%S")
    #_now_string_date = _now_string_date + _now_string_time

    #_file_name_for_saving = "H:\\DATA_WARE_HOUSE\\data\\"+"LNA"+str(_LNA_number)+"SN"+str(_serial_number)+"\\" + "_now_string_Spurious+Screenshot.png"
    _file_name_for_saving = "F:\\LNB" + str(_LNB_number) + "\\" + _now_string + "\\Spurious\\" + "Screenshot_LNA"+str(_LNB_number)+"_"+str(_Branche_number)+".png"
    _N9000a.save_screenshot_png(_file_name_for_saving)

    ## _N9000a.save_screenshot_png('F:/FOU/')

    return(True, _file_name_for_saving)