from influxdb_client import Point
from datetime import datetime

class DataProcessing:
    def __init__(self, node):
        self.node = node
        self.initial_time = str(datetime.now())

    def prepare_data(self, input_data: list[dict[str, any]]):
        ''' Convert the data to the correct format for the database'''
        output_data = []
        for measurement in input_data:
            point = Point(self.node.point_name)
            field_name = None
            field_value = None
            for name, value in measurement.items():
                if name == 'field_name':
                    field_name = value
                elif name == 'field_value':
                    field_value = value
                else:
                    point.tag(name, value)
            if field_name != None and field_value != None:
                point.field(field_name, field_value)
            else:
                raise ValueError('Field name or field value not found in the data')
            point.tag('experiment', self.node.experiment_name + ' ' + self.initial_time)
            output_data.append(point)
        return output_data