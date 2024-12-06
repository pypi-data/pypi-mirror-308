from ...base import BaseNode
from .configuration import Configuration
import json
from opcua import ua
import asyncio

class OPC(BaseNode, Configuration):
    def __init__(self, node_config: dict[str, str], stop_event: asyncio.Event):
        BaseNode.__init__(self, stop_event)
        Configuration.__init__(self, node_config)
    
    async def connect(self):
        try:
            self.create_client()
            self.client.connect()
            self.set_data_location()
        except Exception as e:
            raise ConnectionError(f"An error occurred while connecting to the OPC server: {e}")

    async def disconnect(self):
        try:
            self.client.disconnect()
        except Exception as e:
            print(f"An error occurred while disconnecting from the OPC server: {e}")

    def read(self):
        data = {}
        try:
            for device in self.devices:
                for variable in self.devices[device]['Folder']['Variables']:
                    data[variable.get_display_name().Text] = json.loads(variable.get_value()) ## include variable name in dictionary
            #data['Timestamp'] = str(datetime.now())
            return data
        except Exception as e:
            print(f"An error occurred while reading the data: {e}")

    def write(self, data: dict[str, any]): ## include check if variable exists in the server/device
        try:
            for variable_name, variable_value in data.items():
                for device in self.devices:
                    for variable in self.devices[device]['Folder']['Variables']:
                        if variable.get_display_name().Text == variable_name:
                            json_variant = ua.DataValue(ua.Variant(json.dumps(variable_value), ua.VariantType.String))
                            variable.set_data_value(json_variant)
        except Exception as e:
            print(f"An error occurred while writing the data: {e}")

