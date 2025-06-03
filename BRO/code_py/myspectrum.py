import sys,os
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

str_IP_spectrum_analyzer = "10.0.9.212"

from gs_instrument import InstrumentDummy
from gs_instrument import CsvWriter

sa=spectrum_analyzer.KeysightCXA(str_IP_spectrum_analyzer)

if len(sys.argv)==1:
    avg_count=2
    frequency_Hz=1e9
    #sweep_time_s=sys.argv[3]
    sweep_points=1001
    frequency_span_Hz=25e6
    rbw=10
    plevel=-50


elif len(sys.argv)==2:
    avg_count=2
    frequency_Hz=sys.argv[1]
    #sweep_time_s=sys.argv[3]
    sweep_points=1001
    frequency_span_Hz=25e6
    rbw=10
    plevel=-50
    
elif len(sys.argv)==3:
    avg_count=1
    frequency_Hz=sys.argv[1]
    #sweep_time_s=sys.argv[3]
    sweep_points=1001
    frequency_span_Hz=sys.argv[2]
    rbw=10000
    plevel=-50
     
    
elif len(sys.argv)==7:
    avg_count=sys.argv[1]
    frequency_Hz=sys.argv[2]
    plevel=sys.argv[3]
    sweep_points=sys.argv[4]
    frequency_span_Hz=sys.argv[5]
    rbw=sys.argv[6]


mytime_start =time.strptime(time.strftime("%Y-%m-%d-%H:%M:%S") , "%Y-%m-%d-%H:%M:%S")
mytime=time.strptime(time.strftime("%Y-%m-%d-%H:%M:%S") , "%Y-%m-%d-%H:%M:%S")
d_time =time.mktime(mytime)-time.mktime(mytime_start)


myfile=(f"spec{time.strftime('%Y-%m-%d_%H%M%S')}")
csv_myfile=myfile+".csv"
png_myfile=myfile+".png"
output = gs_instrument.CsvWriter(csv_myfile)
#sa =gs_instrument.spectrum_analyzer
#sa.reset()  #reset spectrum analyzer
sa.set_frequency_center_Hz(frequency_Hz)   #set frequency
#sa.set_sweep_time_s(sweep_time_s) #set time to record
sa.set_frequency_span_Hz(frequency_span_Hz) #set span bandwidth
sa.set_bandwidth_resolution_Hz(rbw)  #set rbw
sa.set_detector_positive_peak()
sa.set_attenuation_dB(0)
sa.phy.write(f"AVER:COUN {int(avg_count)}")

#sa.set_attenuation_auto()
sa.set_trigger_continuous()
sa.set_reference_level_dBm(plevel) #set power ref level
sa.set_trace_max_hold() #set max hold
sa.set_bandwidth_video_Hz(rbw) #set vbw
sa.set_sweep_points(sweep_points) #set number of points

#while d_time < tot_time: #do sweep for tot_time 
#    mytime=time.strptime(time.strftime("%Y-%m-%d-%H:%M:%S") , "%Y-%m-%d-%H:%M:%S")
#    d_time =time.mktime(mytime)-time.mktime(mytime_start)
    #update reading 
sa.set_trigger_single()
sa.wait_for_operation_complete()
    

f_trace, P_trace = sa.get_trace_xy() #get data
  
  # Save the latest result to a file
records = []
for f, P in zip(f_trace, P_trace):
    record = {
        #"timestamp": mytime,  
        #**external_parameters,
        #**tables,
        #**results,
        "meas_frequency_Hz": f,
        "meas_power_dBm": P,
    }
    records.append(record)
output.write_all(records)
sa.save_screenshot_png(png_myfile) #save picture

