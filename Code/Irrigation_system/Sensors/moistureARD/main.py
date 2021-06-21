#from ADS1x15 import ADS1115
from ADS1115_Moist_Sensor import ADS1115
import time
ADDRESS = 0x48 #Default ads1115 address

moistSens_1 = ADS1115(ADDRESS)
moistSens_1.start_adc(0)

while(1):
    moistSens_1.read_moist()
    print(moistSens_1.get_moisture())
    time.sleep(1)



