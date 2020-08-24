import json 
import os
import glob
import csv
import pandas as pd


keys_list = []
empty_map = {}
count = 0
path = '/Users/wusongyuan/Desktop/12345'
output_file = open('sample1.csv', 'w')
'''iterating to open each json file within one pointed folder'''
for filename in glob.glob(os.path.join(path, '*.json')):
   with open(os.path.join(os.getcwd(), filename), 'r') as input_file:
       for json_data in input_file.readlines():
           line = json.loads(json_data)
           print(type(line))
           if line['event_type'] == 'asset-searched' or line['event_type'] == 'image-replaced':
               if line['event_type'] == 'image-replaced':
                   target_field = line['event_properties']
                   for element in target_field.keys():
                       keys_list.append(element)
                       empty_map.update({element:target_field[element]})
                   keys_list.append('client_event_time')
                   empty_map.update({'client_event_time':line['client_event_time']})
                   writer = csv.DictWriter(output_file,fieldnames=keys_list)
                   if count == 0:
                       writer.writeheader()
                       count += 1
                   writer.writerow(empty_map)
                   empty_map.clear()
output_file.close()

'''remove duplcates'''
col_names = ['client_event_time','new-image','project-id','old-image','source']
df = pd.read_csv('sample1.csv', usecols= col_names).drop_duplicates(keep='first').reset_index()
df['old-image'] = '\'' + df['old-image'].astype(str) + '\''
df['new-image'] = '\'' + df['new-image'].astype(str) + '\''
df.to_csv('out1.csv', index = False)


                
                
       
       
           