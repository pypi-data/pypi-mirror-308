from .filter.manager import DataFilter
from abc import ABC, abstractmethod
import copy

class BaseDataProcessing(ABC, DataFilter):
    def __init__(self):
        DataFilter.__init__(self)

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
    
    def process(self, data: list[dict[str, any]]) -> list[dict[str, any]]:
        try:
            output_data = []
            if data:
                for item in data:
                    if 'update_data' == item['action']:
                        self.__process_data(item['data'])
                    elif 'set_config' == item['action']:
                        output_data += self._process_config([item])
                    elif 'error' == item['action']:
                        pass
                    else:
                        raise ValueError('Data type not recognized during processing data')
            return output_data
        except Exception as e:
            print('An error occurred during processing data: ', e)

    def __process_data(self, points: list[dict[str, any]]):
        ''' Update the device data with the new values and save them in the database'''
        try:
            if points:
                flat_new_points = self.__flatten_points(points)
                flat_existing_points = self.__flatten_points(self.controller.data)
                updated_points = self.__update_points(flat_new_points, flat_existing_points)
                points_updated = self.__unflatten_points(updated_points)
                self.controller.variables['data'] = self.filter_data(points_updated, self.desired_variables)
        except Exception as e:
            print('An error occurred while processing the data update: ', e)

    def __flatten_points(self, points: list[dict[str, any]]) -> list[dict[str, any]]:
        flattened = []
        for point in points:
            device_name = point['device_name']
            for data in point['data']:
                flattened.append({
                    'device_name': device_name,
                    'field_name': data['field_name'],
                    'field_value': data['field_value']
                })
        return flattened

    def __unflatten_points(self, points: list[dict[str, any]]) -> list[dict[str, any]]:
        unflattened = {}
        for point in points:
            device_name = point['device_name']
            if device_name not in unflattened:
                unflattened[device_name] = {
                    'response': 'get_data',
                    'device_name': device_name,
                    'data': []
                }
            unflattened[device_name]['data'].append({
                'field_name': point['field_name'],
                'field_value': point['field_value']
            })
        return list(unflattened.values())