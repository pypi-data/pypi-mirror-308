from abc import ABC, abstractmethod

class BaseAcquisition(ABC):
    def __init__(self):
        pass

    def run(self) -> list[dict[str, any]]:
        ''' response = [{'response': 'get_data', 'device_name': device_name, 'data': self.data}] '''
        if self.controller.device_manager.get([{'action': 'get_data'}])[0]['data']:
            output = [{'action': 'update_data', 'data': self.controller.device_manager.get([{'action': 'get_data'}])}]
        else: 
            output = []
        return output