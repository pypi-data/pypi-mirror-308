from abc import ABC, abstractmethod

class BaseAcquisition(ABC):
    def __init__(self):
        pass

    async def run(self) -> list[dict[str, any]]:
        if self.device.device_type == 'simulated':
            data = self.device.model.run()
            return data
        elif self.device.device_type == 'real':
            data = await self.check_buffer()
            return data
                
    def process_request(self, request: dict[str, any]) -> list[dict[str, any]]:
        ''' convert data to the right format (power to voltage, etc.) '''
        try:
            data = {}
            if request:
                if 'set_config' == request['action']:
                    data['action'] = request['action']
                    data['data'] = self._acquire_config(request['data'])
                else:
                    raise ValueError('Invalid request type')
                return [data]
        except Exception as e:
            print('An error occurred during processing request: ', e)

    async def check_buffer(self) -> list[dict[str, any]]:
        data = self.filter_messages(self.device.node.buffer)
        return data
            