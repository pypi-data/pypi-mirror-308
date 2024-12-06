from abc import ABC, abstractmethod

class BaseCommandManager(ABC):
    def __init__(self):
        pass

    def get_command(self, data: list[dict[str, any]]):
        ## we check what config has changed and then we get the command to execute
        command_list = self.check_config(data)
        return command_list

    def check_config(self, data: list[dict[str, any]]):
        ''' Check data and return the command to execute '''
        config_changed = []
        config_changed += self.compare_data(data, self.device.config)
        command_list = self.search_commands(config_changed)
        return command_list