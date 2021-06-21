from Sensors.humTempSHT31D.SHT31D_HumTemp_Sensor import SensorSHT31D
from Sensors.moistureARD.ADS1115_Moist_Sensor import ADS1115
from Logger.data_logger import IrrLogger
from datetime import datetime
from storage import irrData
import time
import threading
import sys
import os
#import GPIO
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

#Globals
#Watering Time (s)
pump_time = 7
#Sensors variables
HT_Sensor_ADDR = [
    0x44,
    0x45   
]
M_Sensor_ADDR = [
    0x48,
    0x49,
    0x4A,
    0x4B
]
ADC_channel = [0,1,2,3] #Connect up to 4 moist sensors per ADC 

#Paths
project_path = None
logFile_path = None

#Thread variables
start_pump = False
start_system = True
log = None

#setup GPIO interface
GPIO_channel = 7 #GPIO4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#define irrigation data storage object
data = irrData()

def moisture_controller():
    #Global variables
    global start_pump
    global start_system
    global log
    global project_path
    global data
    #local variables
    moisture_level = 0
    timestamp = time.time() + 60
    date_time = datetime.now()
    log_filename = date_time.strftime('%y%m%d')
    data.start_date = date_time.strftime('%d/%m/%y %H:%M')
    #define sensor objects
    temp_hum_sens_1 = SensorSHT31D(HT_Sensor_ADDR[0])
    moist_sens_1 = ADS1115(M_Sensor_ADDR[0])
    #start moist_sensor ADC in continous mode
    moist_sens_1.start_adc(ADC_channel[0])
    #Start contol loop
    log.write_to_log(log_filename, 'INFO: P4U system has started\n')
    while(start_system):
        #Get Setpoint
        data.setpoint = int(log.read_from_json(project_path))
        #Get temperature and hum
        try:
            temp_hum_sens_1.i2c_data()
            data.temperature = int(temp_hum_sens_1.get_temp())
            data.humidity = int(temp_hum_sens_1.get_hum())
            #Get moisture level
            moist_sens_1.read_moist()
            moisture_level = moist_sens_1.get_moisture()
        except:
            print('Error- One of the sensing units underwent an error')
        #Convert to percentage
        data.moisture_level = int((moisture_level / 15500.00) * 100)
        #check mositure level
        if(data.moisture_level < data.setpoint and data.moisture_level != 0):
            print('pump started - moist: {} setpoint: {}'.format(data.moisture_level, data.setpoint))
            start_pump = True
        #write to log after 1 minute
        if(time.time() >= timestamp):
            log.write_to_log(log_filename, 'Moisture:  {:}%\t'.format(data.moisture_level) + 'Temp: {:.2f}\t'.format(data.temperature) + 'Hum:  {:.2f}\n'.format(data.humidity))
            timestamp = time.time() + 60
        #Write to json data
        log.write_to_json(data, project_path)
        #print to user
        print('Moisture:  {:}%\t'.format(data.moisture_level) + 'Temp: {:.2f}\t'.format(data.temperature) + 'Hum:  {:.2f}'.format(data.humidity))
        #sleep for 1 seconds
        time.sleep(1)
    log.write_to_log( log_filename, 'INFO: P4U system has stopped\n')

def pump_controller():
    #Global variables
    global start_pump
    global GPIO_channel
    global log
    global data
    global pump_time
    #Configure GPIO pin to start pump
    GPIO.setup(GPIO_channel, GPIO.OUT, initial = GPIO.LOW)
    #Start control loop
    while(start_system):
        #check if pump was activated
        if(start_pump):
            #Save date and time
            current = datetime.now()
            data.last_cycle = current.strftime('%d/%m/%y %H:%M')
            #Set the pump to ON 
            print('Plants are being watered :) - ' + data.last_cycle)
            log.write_to_log('irrigation_cycle', '--Plants Watered--\n')
            GPIO.output(GPIO_channel, GPIO.HIGH)
            time.sleep(pump_time)
            GPIO.output(GPIO_channel, GPIO.LOW)
            start_pump = False

#This function retrieves the directory path of this script
def set_local_path():
    global logFile_path
    global project_path
    #retrieve the realpath to this folder
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = str(current_dir)
    logFile_path = project_path + '/Logger/'

def main():
    print('system has started')
    #define global variables
    global start_system
    global log
    #set the project and logfile paths
    set_local_path()
    #init logfile object
    log = IrrLogger(logFile_path)
    #define threads
    moisture_thread = threading.Thread(target=moisture_controller)
    pump_thread = threading.Thread(target=pump_controller)
    #start threads
    moisture_thread.start()
    pump_thread.start()
    GPIO.setup(11, GPIO.OUT, initial = GPIO.HIGH)
    try:
        while(1):
            pass
            #wait for keyboard interrupt
    except KeyboardInterrupt:
        #stop threads
        start_system = False
        #wait for threads to finish
        moisture_thread.join()
        pump_thread.join()
    GPIO.output(11, GPIO.LOW)
    
if __name__ == '__main__':
    main()
