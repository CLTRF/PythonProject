
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


def save_to_excel(patterns_obj, filename = 'Default_XLS'):

    from openpyxl import load_workbook
    from openpyxl import Workbook
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

    '''
    Saves selected patterns to an Excel file

    Args:
        patterns_obj (object): object of class Patterns. See\
                :class:`~includes.patterns`
        pat_inds (list): List of integers of the patterns to be stored
        field (str): string describing the field to be stored. See\
                :func:`~includes.field_operations.convert_field`
        field_format (str): field format of the field to be stored. See\
                :func:`~includes.field_operations.convert_field_format`
        filename (str): Filename to use. The file will be stored in the output folder. If a file of\
            the same name exists new sheets will be added. If the file does not exist it will be\
            created.
    '''
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = 'output//'+filename+'.xlsx'
    if os.path.isfile(filename):
        workbook = load_workbook(filename)
    else:
        workbook = Workbook()

##    temp_field,_,context = patterns_obj.(pat, field, field_format)

    worksheet = workbook.create_sheet(title=str(pat)+'_'+field+'_'+field_format)
##    __fill_worksheet(worksheet, context, temp_field)   .Gain

    workbook.save(filename)