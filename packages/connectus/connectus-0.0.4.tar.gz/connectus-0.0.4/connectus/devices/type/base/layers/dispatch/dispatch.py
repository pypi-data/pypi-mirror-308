from abc import ABC, abstractmethod

class BaseDispatch(ABC):
    def __init__(self):
        pass
    
    def send_command(self, data: dict[str, any], node_params: dict[str, any]):
        self.device.node.write(data, node_params)