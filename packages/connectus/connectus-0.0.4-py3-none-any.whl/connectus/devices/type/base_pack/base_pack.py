from abc import ABC, abstractmethod
from .configuration import Configuration

class BasePack(ABC, Configuration): ## don't have node implementation
    def __init__(self, name: str, device_type: str, node_params: dict[str, str] = None):
        self.name = name
        self.device_type = device_type
        self.node_params = node_params
        self.node = None
        self.devices = {}
        Configuration.__init__(self)

    @abstractmethod
    def run(self):
        pass

    def get(self, request: list[dict[str, str]]) -> list[dict[str, any]]:
        ''' request = [{'action': 'get_data'}]
            response = [{'response': 'get_data', 'device_name': device_name, 'data': [{...}, {...}]}] '''
        try:
            output = []
            for _, device in self.devices.items():
                    output += device.get(request)
            return output
        except Exception as e:
            print('An error occurred during get request: ', e)
    
    def set(self, request: list[dict[str, any]]):
        ''' request = [{'action': 'set_config', 'data': [{'field_name': name, 'field_value': value}]}] '''
        try:
            for item in request:
                for point in item['data']:
                    for _, device in self.devices.items():
                        if device.name == point['device_name']:
                            device.set([point])
        except Exception as e:
            print('An error occurred during set request: ', e)