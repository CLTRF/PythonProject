"""
This function detect the board the correctly responding
and return serial number, port and temperature
the argument is lna mumber: lna_no
"""
import sys, os
sys.path.insert(1, 'C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include')
import time
import lna_aadetect as aa_function
from aardvark_py import *

def LNA_Identification(lna_no):

    aa_find_devices(1)
    handle = aa_open(0)
    aa_features(handle)
    #aa_close(handle)
    I2C_BITRATE = 100 # kHz
    _number_of_temperature_measurments = 1
    _status                            = False
    cTemp                              = 0
    _port                              = 0
    _inuse                             = ''
    _unique_id                         = 0

    _port, _inuse, _unique_id = aa_function.detect()

    if (_inuse == '(in-use)'):
        _status = True

        aa_configure(handle,  AA_CONFIG_SPI_I2C)

    # Enable the I2C bus pullup resistors (2.2k resistors).
    # This command is only effective on v2.0 hardware or greater.
    # The pullup resistors on the v1.02 hardware are enabled by default.
        aa_i2c_pullup(handle, AA_I2C_PULLUP_BOTH)

    # Power the board using the Aardvark adapter's power supply.
    # This command is only effective on v2.0 hardware or greater.
    # The power pins on the v1.02 hardware are not enabled by default.
        aa_target_power(handle, AA_TARGET_POWER_BOTH)

    # Set the bitrate
        bitrate = aa_i2c_bitrate(handle, I2C_BITRATE)


    # TMP100 address, 0x4F(79)
    # Select configuration register, 0x01(01)
    #		0x60(96)	Continuous conversion, comparator mode, 12-bit resolution
        data_out = array('B', [0, 0])

        if lna_no==1:
            addr=0x48 #lna #1
        elif lna_no==2:
            addr=0x4A #lna #2
        elif lna_no==3:
            addr=0x4B #lna #3
        elif lna_no==4:
            addr=0x4C #lna #4

# Configure I/O expander lines as outputs

        print("LNA no: {0}\n".format(lna_no))
        for i in range(0,_number_of_temperature_measurments):
            data_out[0] = 0x01
            data_out[1] = 0x60
            res = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, data_out) #config
            data_out[0] = 0x00
            data_out[1] = 0x60
            res = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, data_out) #temperature
            time.sleep(0.5)

            # TMP100 address, 0x4F(79)
            # Read data back from 0x00(00), 2 bytes
            # temp MSB, temp LSB

            length=2
            (cc,data_out) = aa_i2c_read(handle,addr,AA_I2C_NO_FLAGS, length)
            #print data_out


            # Convert the data to 12-bits
            temp = (data_out[0] * 256 + (data_out[1] & 0xF0)) / 16
            if temp > 2047 :
    	        temp -= 4096
            cTemp = temp * 0.0625
            #fTemp = cTemp * 1.8 + 32

            # Output data to screen
            print ("Temperature in Celsius is : %.2f C" %cTemp)


    return _status, cTemp,  _port, _inuse, _unique_id