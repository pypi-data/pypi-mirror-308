import asyncio

class DeviceManager():
    def __init__(self, stop_event: asyncio.Event, step_factor: float = 1.0):
        self.devices = []
        self.stop_event = stop_event
        self.step_factor = step_factor
    
    def add(self, device):
        try:
            item = {}
            item['name'] = device.name
            item['instance'] = device
            self.devices.append(item)
        except Exception as e:
            print('An error occurred adding a device: ', e)

    async def start(self):
        print('Device Manager is running')
        update_bundle = []
        for device in self.devices:
            update = asyncio.create_task(self.__run_device(device['instance']))
            update_bundle.append(update)
        await asyncio.gather(*update_bundle)
    
    def get(self, request: list[dict[str, any]]) -> list[dict[str, any]]: ## future improvement: get data from a specific device
        ''' request = [{'action': 'get_data'}]
            response = [{'response': 'get_data', 'device_name': device_name, 'data': self.data}] '''
        try:
            data = []
            for item in request:
                for device in self.devices:
                        data += device['instance'].get([item])
            return data
        except Exception as e:
            print('An error occurred during get request: ', e)
    
    def set(self, request: list[dict[str, any]]):
        ''' request = [{'action': 'set_config', 'device_name': device_name, 'data': [{'field_name': field_name, 'field_value': field_value}, {...}]}] '''
        try:
            for item in request:
                matched_device = None
                for device in self.devices:
                    if device['name'] == item['device_name']:
                        device['instance'].set([item])
                        matched_device = device
                        break
                if matched_device is None:
                    raise ValueError(f'Device not found in set request: {item["device_name"]}')
                    
        except Exception as e:
            print('An error occurred during set request: ', e)

    async def __run_device(self, device):
        while not self.stop_event.is_set():
            await device.run()
            await asyncio.sleep(device.step_time*self.step_factor)