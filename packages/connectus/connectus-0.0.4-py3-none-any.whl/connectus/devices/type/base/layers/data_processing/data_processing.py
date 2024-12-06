from .commands.manager import BaseCommandManager
from .filter.manager import DataFilter
import asyncio
import copy
import time

class BaseDataProcessing(BaseCommandManager, DataFilter):
    def __init__(self):
        BaseCommandManager.__init__(self)
        DataFilter.__init__(self)

    def process_data(self, data: list[dict[str, any]]):
        try:
            if data:
                for item in data:
                    if 'update_config' == item['action']:
                        self.__process_config(item['data'])
                    elif 'update_data' == item['action']:
                        self.__process_data(item['data'])
                    elif 'set_config' == item['action']:
                        if self.device.device_type == 'simulated':
                            self.__process_config(item['data'])
                        elif self.device.device_type == 'real':
                            commands = self.get_command(item['data'])
                            self.device.dispatch.send_command(commands, self.device.node_params)
                    elif 'error' == item['action']:
                        pass
                    else:
                        raise ValueError('Data type not recognized during processing data')
        except Exception as e:
            print('An error occurred during processing data: ', e)

    def __process_config(self, points: list[dict[str, any]]):
        ''' Check if the configuration is correct and update the device configuration'''
        try:
            if points:
                points_updated = self.__update_points(points, self.device.config)
                self.device.variables['config'] = self.filter_data(points_updated, self.desired_variables)
        except Exception as e:
            print('An error occurred while processing the configuration: ', e)
    
    def __process_data(self, points: list[dict[str, any]]):
        ''' Update the device data with the new values and save them in the database'''
        try:
            if points:
                points_updated = self.__update_points(points, self.device.data)
                self.device.variables['data'] = self.filter_data(points_updated, self.desired_variables)
                asyncio.create_task(self.device.managers['node'].save(points_updated))
        except Exception as e:
            print('An error occurred while processing the data update: ', e)

    def __update_points(self, new_points: list[dict[str, any]], existing_points: list[dict[str, any]]):
        ''' Compare the new values with the previous ones and update or add the value'''
        # Create a map of existing points without 'field_value' for comparison
        existing_points_map = copy.deepcopy(existing_points)
        if existing_points_map:
            for point in existing_points_map:
                del point['field_value']
        # Process new points
        for new_point in new_points:
            field_value = new_point.pop('field_value')  # Temporarily remove 'field_value' for comparison
            if new_point in existing_points_map:
                # If the new point matches an existing point (excluding 'field_value'), update the existing point's 'field_value'
                existing_points[existing_points_map.index(new_point)]['field_value'] = field_value
            else:
                # If the new point does not match any existing point, add it back with 'field_value' and append to existing_points
                new_point['field_value'] = field_value
                existing_points.append(new_point)
        return existing_points
    
    def compare_data(self, new_data: list[dict[str, any]], old_data: list[dict[str, any]]):
        points_changed = []
        existing_points_map = copy.deepcopy(old_data)
        if existing_points_map:
            for point in existing_points_map:
                del point['field_value']
        # Process new points
        for new_point in new_data:
            new_value = new_point.pop('field_value')  # Temporarily remove 'field_value' for comparison
            if new_point in existing_points_map:
                old_value = old_data[existing_points_map.index(new_point)]['field_value']
                if new_value != old_value:
                    new_point['field_value'] = new_value
                    points_changed.append(new_point)
        return points_changed