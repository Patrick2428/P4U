import smbus2
import time
from smbus2 import SMBus
#The following class is used for I2C communication with the SHT31-D humidity and temperature sensor
#Author: Patrick Tietz
#Project: Planting4U
#University: HAN University of Applied Sciences

POINTER_CONVERSION = 0x00
POINTER_CONFIG = 0x01

CONFIG_MODE_SINGLE = 0x0100
CONFIG_MODE_CONTINUOUS = 0x0000

CONFIG_OS_SINGLE = 0x8000
CONFIG_MUX_OFFSET = 12
CONFIG_DR = 0x0080
CONFIG_COMP_QUE_DISABLE = 0x0003


CONFIG_GAIN = {
    2/3: 0x0000,
    1:   0x0200,
    2:   0x0400,
    4:   0x0600,
    8:   0x0800,
    16:  0x0A00
}

class ADS1115:
    def __init__(self, _address, _busNum = 1):
        self.address = _address 
        self.busNum = _busNum
        self.bus = smbus2.SMBus(self.busNum)
        self.moist = 0

    def send_data(self, _register, _data):
        #Send a block of data- function_format(address, offset/register, data)
        self.bus.write_i2c_block_data(self.address, _register, _data)

    def send_byte(self, _register, _data):
        #Write a byte value to the allocated adress- function_format(address, offset/register, data)
        self.bus.write_byte_data(self.address, _register, _data)

    def read_data(self, _register, _bytes = 2):
        # Read a block of data- function_format(address, offset/register,bytes)
        data = self.bus.read_i2c_block_data(self.address, _register, _bytes)
        return data
    
    def start_adc(self, _channel, _gain = 1, _data_rate = 128):
        #configure adc A0
        #config_single = 0b1100001110000011 #single conversion
        #config_continous = 0b1100001010000011 #continous conversion
       #Get out of power mode
        config = CONFIG_OS_SINGLE
        #Select the channel to read from (A0->A3)
        chan = _channel + 0x04
        config |= (chan & 0x07) << CONFIG_MUX_OFFSET
        #Set the gain
        config |= CONFIG_GAIN[_gain]
        #Set the mode
        config |= CONFIG_MODE_CONTINUOUS
        #Set the sampling/data rate
        config |= CONFIG_DR
        #Deisable comparator mode
        config |= CONFIG_COMP_QUE_DISABLE
        #Send configuration to ADS1115
        self.send_data(POINTER_CONFIG, [(config >> 8 ) & 0xFF, config & 0xFF])
        #wair until data was processed
        time.sleep(1.0/_data_rate+0.0001)

    def read_moist(self):
        bin_data = self.read_data(POINTER_CONVERSION, 4)
        self.moist = self.convert_data(bin_data[1], bin_data[0])
    
    def convert_data(self, _data_low, _data_high):
        #Convert i2C adc data to decimal data
        # Convert to 16-bit signed value.
        value = ((_data_high & 0xFF) << 8) | (_data_low & 0xFF)
        # Check for sign bit and turn into a negative value if set.
        if value & 0x8000 != 0:
            value -= 1 << 16
        #Convert to percentage
        #Max 15500 
        #Min 0 
        #value_per = (value / 15500) * 100
        return(value)     
    
    def get_moisture(self):
        #return the temperature variable
        return self.moist
        
    
