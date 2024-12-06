from .configuration import Configuration
from abc import ABC, abstractmethod

class BaseDevice(ABC, Configuration):
    def __init__(self, name: str, device_type: str, node_params: dict[str, str] = None):
        self.name = name
        self.device_type = device_type
        self.node_params = node_params
        self.node = None
        Configuration.__init__(self)

    def get(self, request: list[dict[str, str]]) -> list[dict[str, any]]:
        ''' request = [{'action': 'get_data'}]
            response = [{'response': 'get_data', 'device_name': device_name, 'data': [{...}, {...}]}] '''
        try:
            response = []
            for item in request:
                if item['action'] == 'get_data':
                    response += [{'response': item['action'], 'device_name': self.name, 'data': self.data}]
                elif item['action'] == 'get_config':
                    response += [{'response': item['action'], 'device_name': self.name, 'data': self.config}]
                else:
                    raise ValueError('Request not recognized')
            return response
        except Exception as e:
            print('An error occurred during get request: ', e)

    def set(self, request: list[dict[str, any]]): ## improve this
        ''' request = [{'action': 'set_config', 'data': [{'field_name': name, 'field_value': value}]}] '''
        try:
            for item in request:
                data = self.acquisition.process_request(item)
                self.data_processing.process_data(data) ## improve this
        except Exception as e:
            print('An error occurred during set request: ', e)

    async def run(self):
        data = await self.acquisition.run()
        self.data_processing.process_data(data)
        self.total_time += self.step_time
