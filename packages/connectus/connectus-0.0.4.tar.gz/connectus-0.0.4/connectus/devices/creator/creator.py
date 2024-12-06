
class DeviceCreator():
    def __init__(self, device_manager, node_creator):
        self.device_manager = device_manager
        self.node_creator = node_creator

    def create(self, instance):
        try:
            self.device = instance
            self.__set_device_manager()
            self.__set_data_manager()
            if self.device.node_params:
                self.__set_node(self.device.node_params)
        except Exception as e:
            print("An error occurred while creating device: ", e)
            
    def __set_device_manager(self):
        try:
            self.device.add_device_manager(self.device_manager)
        except Exception as e:
            print('An error occurred while setting the device manager: ', e)

    def __set_data_manager(self):
        try:
            self.device.add_data_manager(self.node_creator.data_manager)
        except Exception as e:
            print('An error occurred while setting the data manager: ', e)
    
    def __set_node(self, node_params: dict[str, str]):
        try:
            node = self.node_creator.create_node(node_params)
            self.device.node = node
        except Exception as e:
            print('An error occurred while setting the node: ', e)