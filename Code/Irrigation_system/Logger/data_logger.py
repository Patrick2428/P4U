import os
import json
from datetime import datetime


class IrrLogger:
    def __init__(self,_path):
        self._path = _path
        self.folder = self._path + '/logs/'
        self.file = None
        #create log directory
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        
    def write_to_log(self, _name ,_data):
        self.file = open(self.folder + str(_name) + '.log','a')
        current_time = datetime.now()
        self.file.write('time:\t' + current_time.strftime('%y/%m/%d - %H:%M:%S') + '\t' +_data)
        self.file.close()

    def write_to_json(self,_data, _path):
        data = {}
        data["Irrigation_data"] ={
            "start_data":  _data.start_date,
            "moisture_setpoint": _data.setpoint,
            "humidity": _data.humidity,
            "last_watercycle": _data.last_cycle,
            "moisture": _data.moisture_level,
            "temperature": _data.temperature
        }

        JSONfile = open(_path + '/../Website/data/irr_data.json', 'w')
        json.dump(data, JSONfile)
    
    def read_from_json(self,_path):
        JSONfile = open (_path + '/../Website/data/sp_data.json', 'r')
        data = json.load(JSONfile)
        setpoint = data['sp']
        return setpoint
        
