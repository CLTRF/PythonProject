#def _NOISE_FIGURE_MEASURMENTS_X_BAND(_str_freq_MHz, _stop_freq_MHz, _IF_BW_MHz, _Nb_Points_Sc, _ENR_dB, _frequency_MHz, _span_MHz, _LNA_no, _LNA_serial_number):
def _NOISE_FIGURE_MEASURMENTS_X_BAND():
    """
   this function measures Noise Figure of the BRO X-BAND LNA using N9000A Spectrum Analyzer.
   it passes:
   start frequency in MHz
   stop frequency in MHz
   Spectrum Analyzer Intermediate Frequency in MHz
   Number of points in scalar unit
   ENR in dB
    """

    # required setup
    # mcu
    # spectrum analyzer N9000A
    # if generator

    # P47-60
    # RF freq 8250 fixed
    # IF power fixed
    # modcon vary
    # plot spur levels as time20.0	30.0
    #
    # 20.0	30.0
    # P47-50
    # RF freq 8250 fixed
    # IF power fixed
    # plot spur levels as time

    import gs_instrument
    from gs_instrument import spectrum_analyzer

    import sys, os
    sys.path.insert(1, '/home/max/python/myimport')
    import numpy as np
    #import SMU200
    #import N9000A
    import time
    import json
    import datetime
    import select

    #######################20.0	30.0#######################################################
    #                           main program
    ##############################################################################

    # TCP settings
    SMU200_host = '10.0.9.173'
    N9000a_host = '10.0.9.212'
    # N9000a_host='10.0.9.102'

    # setup1 P47-10
    LO_freq = 3365  # error of pll setting #
    # IF frequnecy
    IF_freq = 3022.5
    time_nop = 5
    if_power = -20
    myoffset = 17  # need to be specified
    mod_choice = 0

    # initalization of instruments
    #N9000b = N9000A.N9000(N9000a_host)
    _N9000a=spectrum_analyzer.KeysightCXA(N9000a_host)
    #SMU200b = SMU200.SMU200(SMU200_host)

    #SMU200b.single_freq(-15, IF_freq)  # set iF
    #SMU200b.RF_on()
    # RF frequnecy
    RF_range = [9345, 9450]  # MHz
    IF_range = [3295, 3405]
    LO = 6045
    cal = True

    if cal == True:
        #_N9000a.NF_meas_converter(IF_range[0], IF_range[1], 2, 16, LO, 41)
        _N9000a.NF_meas(IF_range[0], IF_range[1], 2, 16, 41)

        print("Do calibration, hit enter when ready to capture data ")
        #while True:
            #if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                #line = raw_input()
        line = input()
                #time.sleep(5)

    for _LNB_no in range(0, 4):
        print("Connect cable to LNB{0} to Do measurements and hit ready to capture data ".format(_LNB_no))
        line = input()
        for _LNB_level_2 in range(1, 5, 1):

                _LNB_number = _LNB_no + 1

                print("#1.Connect cable to LNA{0} to Do measurements and hit ready to capture data ".format(_LNB_number))
                line = input()
                print("#2.Connect cable to LNA{0} to Do measurements and hit ready to capture data ".format(_LNB_number))
                line = input()
                # time.sleep(5)

                _now = datetime.datetime.now()
                _now_string = _now.strftime("%d%m%y_%H%M%S")

                _file_name_for_saving = "H:\\DATA_WARE_HOUSE\\data\\" + "LNB" + str(_LNB_number) + "\\BRANCHE" + str(_LNB_level_2) + "\\NF\\Screenshot.png"
                xxx = "H:\\DATA_WARE_HOUSE\\data\\" + "LNB" + str(_LNB_number) + "\\BRANCHE" + str(_LNB_level_2) + "\\NF\\" + "NF.csv".format(_LNB_number)

                ##_file_name_for_saving = "H:\\DATA_WARE_HOUSE\\data\\" + "LNA" + str(_LNA_no) + "\\SN" + str(_LNA_serial_number) + "\\Screenshot.png"
                print(_file_name_for_saving)

                _N9000a.save_screenshot_png(_file_name_for_saving)

                NF, Gain = list(_N9000a.get_NF())
                # xxx = "F:\\LNA"+str(_LNA_no)+"\\NF\\"+"SN"+str(_LNA_serial_number)+"{0}.csv".format(_LNA_no)
                ##xxx = "H:\\DATA_WARE_HOUSE\\data\\"+"LNA"+str(_LNA_no)+"\\SN"+str(_LNA_serial_number)+"\\"+"{0}.csv".format(_LNA_no)

                print(xxx)
                csv_file = open(xxx, mode='w')
                for i in range(0, len(NF)):
                    data = "{0},{1}\n".format(NF[i], Gain[i])
                    csv_file.write(data)
                csv_file.close()

        return (True, csv_file)

def _NOISE_FIGURE_MEASURMENTS(_str_freq_MHz, _stop_freq_MHz, _IF_BW_MHz, _Nb_Points_Sc, _ENR_dB, _frequency_MHz, _span_MHz, _LNA_no, _LNA_serial_number):

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
    import datetime
    from math import inf
    from types import SimpleNamespace
    import numpy as np
    import gs_instrument
    from gs_instrument import spectrum_analyzer

    import numpy as np
    #import SMU200
    import time
    import json
    import select
    from gs_instrument import InstrumentDummy
    from gs_instrument import CsvWriter

## Test Spec
    _str_freq_MHz   =   3000
    _stop_freq_MHz  =   3100
    _IF_BW_MHz      =   2
    _Nb_Points_Sc   =   40
    _ENR_dB         =   6
    _Frequency_Hz           =   1000000000.0 # 1 GHz
    _Span_Hz                =   25000000.0 #25 MHz
    _Rbw_Hz                 =   10
    _Plevel_dB              =   -50
    _Sweep_points           =   1001
    _Attenuation_dB         =   0
    _Detector_Positive_Peak =   True
    _path_to_usb_drive      =   "F:\\LNA1\\"
    _Path_to_screen_shot    =   'F:\\'
    csv_file = ""

    #required setup
    #mcu
    #spectrum analyzer N9000A
    #if generator


    #P47-60
    #RF freq 8250 fixed
    #IF power fixed
    #modcon vary
    #plot spur levels as time20.0	30.0
    #
    #20.0	30.0
    #P47-50
    #RF freq 8250 fixed
    #IF power fixed
    #plot spur levels as time

    # local variables Initialisation
    _str_IP_spectrum_analyzer = "10.0.9.212"
    _N9000a=spectrum_analyzer.KeysightCXA(_str_IP_spectrum_analyzer)

    # RF frequency
    RF_range=[_str_freq_MHz, _stop_freq_MHz] #MHz
    _cal=True

    #   Init
    myfile=(f"spec{time.strftime('%Y-%m-%d_%H%M%S')}")
    csv_myfile= _path_to_usb_drive + myfile+".csv"
    png_myfile= _path_to_usb_drive +  myfile+".png"

    output = gs_instrument.CsvWriter(csv_myfile)
    #### CLT _N9000a.reset()
    ######_N9000a.set_frequency_center_Hz(_Frequency_Hz)   #set frequency
    #_N9000a.set_sweep_time_s(sweep_time_s) #set time to record
    _N9000a.set_frequency_span_Hz(_Span_Hz) #set span bandwidth
    _N9000a.set_bandwidth_resolution_Hz(_Rbw_Hz)  #set rbw
    if (_Detector_Positive_Peak == True):
        _N9000a.set_detector_positive_peak()
    _N9000a.set_attenuation_dB(_Attenuation_dB)

    if _cal==True:
        _N9000a.NF_meas(RF_range[0], RF_range[1], 2, 8, 41)
        #temp_N9000A.NF_meas(_N9000a,RF_range[0],RF_range[1],2,8,41)
        print("Do calibration, hit enter when ready to capture data ")

        line = input()

        serial_number_count = 0

        for _LNA_level_1 in range(0, 4, 1):
            for _LNA_level_2 in range(0, 4, 1):

                _LNA_number = _LNA_level_1 + 1
                _LNA_no = _LNA_number
                _LNA_serial_number = 93 + serial_number_count


                serial_number_count+=1

                print("#1.Connect cable to LNA{0} to Do measurements and hit ready to capture data ".format(_LNA_no))
                line = input()
                print("#2.Connect cable to LNA{0} to Do measurements and hit ready to capture data ".format(_LNA_no))
                line = input()
                #time.sleep(5)

                _now = datetime.datetime.now()
                _now_string = _now.strftime("%d%m%y_%H%M%S")

                _file_name_for_saving = "F:\\LNA"+str(_LNA_no)+"\\NF\\"+"SN"+str(_LNA_serial_number)+"\\Screenshot.png"
                ##_file_name_for_saving = "H:\\DATA_WARE_HOUSE\\data\\" + "LNA" + str(_LNA_no) + "\\SN" + str(_LNA_serial_number) + "\\Screenshot.png"
                print(_file_name_for_saving)

                _N9000a.save_screenshot_png(_file_name_for_saving)


                NF, Gain = list(_N9000a.get_NF())
    #xxx = "F:\\LNA"+str(_LNA_no)+"\\NF\\"+"SN"+str(_LNA_serial_number)+"{0}.csv".format(_LNA_no)
    ##xxx = "H:\\DATA_WARE_HOUSE\\data\\"+"LNA"+str(_LNA_no)+"\\SN"+str(_LNA_serial_number)+"\\"+"{0}.csv".format(_LNA_no)
                xxx = "H:\\DATA_WARE_HOUSE\\data\\" + "LNA" + str(_LNA_no) + "\\SN" + str(_LNA_serial_number) + "\\" + "NF.csv".format(_LNA_no)
                print(xxx)
                csv_file = open(xxx, mode='w')
                for i in range(0, len(NF)):
                    data="{0},{1}\n".format(NF[i],Gain[i])
                    csv_file.write(data)
                csv_file.close()

    return (True, csv_file)

def _NOISE_FIGURE_MEASURMENTS_X_BAND2():

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
    import datetime
    from math import inf
    from types import SimpleNamespace
    import numpy as np
    import gs_instrument
    from gs_instrument import spectrum_analyzer

    import numpy as np
    #import SMU200
    import time
    import json
    import select
    from gs_instrument import InstrumentDummy
    from gs_instrument import CsvWriter

    # Legacy from Max
    # setup1 P47-10
    LO_freq = 3365  # error of pll setting #
    # IF frequnecy
    IF_freq = 3022.5
    time_nop = 5
    if_power = -20
    myoffset = 17  # need to be specified
    mod_choice = 0
    # RF frequnecy
    RF_range = [9345, 9450]  # MHz
    IF_range = [3295, 3405]
    LO = 6045
    cal = True

    _str_freq_MHz       =   IF_range[0]
    _stop_freq_MHz      =   IF_range[1]
    _IF_BW_MHz = 2
    _Nb_Points_Sc = 40
    _ENR_dB = 6
    _Frequency_Hz = 1000000000.0  # 1 GHz
    _Span_Hz = 25000000.0  # 25 MHz
    _Rbw_Hz = _IF_BW_MHz * 1e6
    _Plevel_dB = -20
    _Sweep_points = 1001
    _Attenuation_dB = 0
    _Detector_Positive_Peak = True
    _path_to_usb_drive      = 'F:\\LNB1\\'
    _Path_to_screen_shot    = 'F:\\LNB1\\'
    csv_file = ""

    # local variables Initialisation
    _str_IP_spectrum_analyzer = "10.0.9.212"
    _N9000a=spectrum_analyzer.KeysightCXA(_str_IP_spectrum_analyzer)

    #_N9000a.reset()

    # RF frequency
    RF_range=[_str_freq_MHz, _stop_freq_MHz] #MHz
    _cal=True

    #   Init
    myfile=(f"spec{time.strftime('%Y-%m-%d_%H%M%S')}")
    csv_myfile= _path_to_usb_drive + myfile+".csv"
    png_myfile= _path_to_usb_drive +  myfile+".png"

    output = gs_instrument.CsvWriter(csv_myfile)
    #### CLT _N9000a.reset()
    ######_N9000a.set_frequency_center_Hz(_Frequency_Hz)   #set frequency
    #_N9000a.set_sweep_time_s(sweep_time_s) #set time to record
    _N9000a.set_frequency_span_Hz(_Span_Hz) #set span bandwidth
    _N9000a.set_bandwidth_resolution_Hz(_Rbw_Hz)  #set rbw
    if (_Detector_Positive_Peak == True):
        _N9000a.set_detector_positive_peak()
    _N9000a.set_attenuation_dB(_Attenuation_dB)

    if _cal==True:
        _N9000a.NF_meas(IF_range[0], IF_range[1], 2, 8, 41)
        #temp_N9000A.NF_meas(_N9000a,RF_range[0],RF_range[1],2,8,41)
        print("Do calibration, hit enter when ready to capture data ")

        line = input()

        serial_number_count = 0

        for _LNB_no in range(1, 5, 1):
            print("Connect cable to LNB{0} to Do measurements and hit ready to capture data ".format(_LNB_no))
            line = input()
            for _LNB_level_2 in range(1, 5, 1):

                print("#1.Connect cable to Branche{0} to Do measurements and hit ready to capture data ".format(_LNB_level_2))
                line = input()
                time.sleep(5)

                _now = datetime.datetime.now()
                _now_string = _now.strftime("%d%m%y_%H%M%S")

                _file_name_for_saving = "F:\\" + "LNB" + str(_LNB_no) + "\\BRANCHE" + str(_LNB_level_2) + "\\NF\\" + "Screenshot.png"
                ##xxx = "F:/" + "LNB" + str(_LNB_no) + "/BRANCHE" + str(_LNB_level_2) + "/NF/" + "NF.csv".format(_LNB_no)
                xxx = "H:\\DATA_WARE_HOUSE\\data\\" + "LNB" + str(_LNB_no) + "\\BRANCHE" + str(_LNB_level_2) + "\\" + "NF.csv".format(_LNB_no)
                print(_file_name_for_saving)

                _N9000a.save_screenshot_png(_file_name_for_saving)
                NF, Gain = list(_N9000a.get_NF())
                print(xxx)
                csv_file = open(xxx, mode='w')
                for i in range(0, len(NF)):
                    data="{0},{1}\n".format(NF[i],Gain[i])
                    csv_file.write(data)
                csv_file.close()

        return (True, csv_file)
