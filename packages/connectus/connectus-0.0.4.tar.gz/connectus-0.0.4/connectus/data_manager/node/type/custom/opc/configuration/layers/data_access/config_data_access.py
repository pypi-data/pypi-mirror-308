class ConfigDataAccess:
    def __init__(self, data_location: dict[str, any]):
        self.data_location = data_location
        self.devices = {}
        self.device = {
            'Node': None,
            'Folder': {
                'Node': None,
                'Variables': None
            }
        }
    
    def set_data_location(self):
        try:
            for device, folder in self.data_location.items():
                self.add_device(device, folder)
        except Exception as e:
            print(f"An error occurred while setting the data location: {e}")

    def add_device(self, device: str, folder: str):
        try:
            self.device['Node'] = self.__search_node(self.client.get_objects_node(), device)
            self.device['Folder']['Node'] = self.__search_node(self.device['Node'], folder)
            self.device['Folder']['Variables'] = self.__get_variables(self.device['Folder']['Node'])
            self.devices[device] = self.device
        except Exception as e:
            print(f"An error occurred while adding the device: {e}")

    def __get_variables(self, node):
        try:
            return node.get_variables()
        except Exception as e:
            print(f"An error occurred while getting the variables: {e}")

    def __search_node(self, node, child_name: str):
        try:
            children_nodes = node.get_children()
            for child_node in children_nodes:
                if child_node.nodeid.Identifier == child_name:
                    return child_node
            raise Exception(f"Node {child_name} not found")
        except Exception as e:
            print(f"An error occurred while searching the node: {e}")