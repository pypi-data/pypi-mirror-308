
class Configuration:
    def __init__(self):
        self.variables = {}
        self.total_time = 0
        self.__set_managers()

    def __set_managers(self):
        self.managers = {'device': None, 'node': None}

    def add_device_manager(self, device_manager):
        self.managers['device'] = device_manager
        self.managers['device'].add(self)
    
    def add_data_manager(self, data_manager):
        self.managers['node'] = data_manager