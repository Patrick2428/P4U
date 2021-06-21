import smbus2
import time
from smbus2 import SMBus
#The following class is used for I2C communication with the SHT31-D humidity and temperature sensor
#Author: Patrick Tietz
#Project: Planting4U
#University: HAN University of Applied Sciences

_TEMP_HUM_REG = 0x00
_START_MES_REG = 0x2C

class SensorSHT31D:
    def __init__(self, _address, _busNum = 1):
        self.address = _address 
        self.busNum = _busNum
        self.bus = smbus2.SMBus(self.busNum)
        self.temp = 0.0
        self.hum =0.0 

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

    def i2c_data(self):
        #Send START condition to sensor
        self.send_byte(_START_MES_REG, 0x06)
        # Read 6 data bytes in the following format [Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC]
        bin_temphum = self.read_data(_TEMP_HUM_REG, 6)
        self.convert_data(bin_temphum)
    
    def convert_data(self, binData):
        #Filter out the MSB and LSB for the Temp and and the hum fro the i2C data block
        tempMSB = '{0:08b}'.format(binData[0])
        tempLSB = '{0:08b}'.format(binData[1])
        humMSB = '{0:08b}'.format(binData[3])
        humLSB = '{0:08b}'.format(binData[4])
        #concatinate the Binary numbers
        bin_temp = tempMSB + tempLSB
        bin_hum = humMSB + humLSB
        #calculate RH
        #RH = 100 * dec(SRH)/(65536-1)
        self.hum = 100.0 * int(bin_hum,2)/(65535.0)
        #calculate T
        #T[*C]= -45 + 175 * dec(ST)/(65536-1)
        self.temp = -45.0 + 175.0 * int(bin_temp,2)/(65535.0)
        
    
    def get_temp(self):
        #return the temperature variable
        return self.temp
    
    def get_hum(self):
        #return the humidity
        return self.hum
        
    
