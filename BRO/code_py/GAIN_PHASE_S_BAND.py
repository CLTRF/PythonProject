def _S_BAND_SPARAMETER(_LNA_no):

    """
   this function measures the S2P parameter for the S Band LNA
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
    from gs_instrument import network_analyzer

    _S2P_file_name          =   []
    _Gain_Phase_Parameter   =   []

    _str_IP_vector_analyzer = "10.0.8.72"
    _ZNB20=network_analyzer.RohdeSchwarzZNB8(_str_IP_vector_analyzer)

    time.sleep(5)
    _now = datetime.datetime.now()
    _now_string = _now.strftime("%d%m%y_%H%M%S")

    _file_name_for_saving_sc = "C:\\" + "LNA" + str(_LNA_no) + "\\"+ "LNA"+str(_LNA_no)+"_" + _now_string +"_Gain_"+"Screenshot.png"
    _file_name_for_saving_S2P = "C:\\" + "LNA" + str(_LNA_no) + "\\" +"LNA"+str(_LNA_no)+"_" + _now_string +"_Gain_"+"Gain.s2p"

    _ZNB20.save_screenshot_png(_file_name_for_saving_sc)
    _data = _ZNB20.save_touchstone(_file_name_for_saving_S2P, trace =1 )

    return (True, _file_name_for_saving_sc,_file_name_for_saving_S2P,_data)