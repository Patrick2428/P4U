from SHT31D_HumTemp_Sensor import SensorSHT31D
import time
#Addressing:
#Short pin ADR with
#GND - 0x44
#VIN - 0x45

#Usage:
#1.Create a Sensor object and pass the assigned sensor address
#2.Call the i2c.data() function dor Single Shot Data Acquisition
#3.Call get_hum() or get.temp() functions to retrieve the humidity or temperatur of the data aquisition

humSense_1 = SensorSHT31D(0x44)
#humSense_2 = SensorSHT31D(0x45)

while(1):
    
    humSense_1.i2c_data()
   # humSense_2.i2c_data()
    print('Sensor1:\thum= {:.2f}\t'.format(humSense_1.get_hum()) + 'Temp={:.2f}'.format(humSense_1.get_temp()))
    #print('Sensor2:\thum= {:.2f}\t'.format(humSense_2.get_hum()) + 'Temp={:.2f}\n'.format(humSense_2.get_temp()))
    time.sleep(1)
