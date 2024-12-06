import pandas as pd

class DataFilter:
    def __init__(self):
        pass

    def filter_data(self, data: list[dict[str, any]], filter_conditions: list[dict[str, any]]) -> dict[str, any]:
        try:
            ''' filter_conditions = [{'field_name': field_name, 'tags': {tag_name1: tag_value1, 'tag_name2': 'tag_value2'}},
                                    {...}] 
                                    
                'tags' is optional '''
            self.df = pd.json_normalize(data, 'data', ['response', 'device_name'])
            filtered_dfs = []
            for condition in filter_conditions:
                field_name = condition['field_name']
                sub_df = self.df[self.df['field_name'] == field_name]
                if 'tags' in condition and condition['tags']:
                    for key, value in condition['tags'].items():
                        sub_df = sub_df[sub_df[key] == value]
                filtered_dfs.append(sub_df)
            if filtered_dfs:
                filtered_df = pd.concat(filtered_dfs)
            else:
                filtered_df = pd.DataFrame()

            filtered_dict = {}
            for device_name, group in filtered_df.groupby('device_name'):
                device_dict = {}
                for _, row in group.iterrows():
                    device_dict[row['field_name']] = row['field_value']
                filtered_dict[device_name] = device_dict

            return filtered_dict
        except Exception as e:
            print('An error occurred during filtering data: ', e)