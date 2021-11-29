
from __Config.Include.Common_Include import *

class DataDaily:
    base_path = settings.BASE_DIR + '/__Security_Data/data_daily/data/'
    
    def write_data(self, date, data = {}):
        with open(f'{self.base_path}{str(date)}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def read_data(self, date):
        data_loaded = {}
        try:
            with open(f'{self.base_path}{date}.json') as data_file:
                data_loaded = json.load(data_file)
            
        except Exception as inst:
            print(inst)
        
        return data_loaded
            

