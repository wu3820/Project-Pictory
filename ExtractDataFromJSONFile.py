import json  
import csv  

'''read image url and image metadata from the json file downloaded 
from AWS
'''
with open('/Users/akshaychalana/Downloads/projects.json') as f_input:
    json_data = json.load(f_input, strict = False)
    """Convert json file to csv file"""
    items_list = json_data['Items']
    '''check whether it is python dict'''
    print(type(items_list))
    '''Storing columns names'''
    fieldnames = set()
    output_dicts = []
    for entry in items_list:
        if 'scenes' in entry.keys():
            inner_list = entry['scenes']['L']
            for element in inner_list:
                row = dict()
                row['image'] = element['M']['image']
                if 'imageMetadata' in element['M'].keys():
                    map3 = json.loads(element['M']['imageMetadata']['S'])
                    for key in map3.keys():
                        row[key] = map3[key]
                row_set = set(row.keys())
                if not row_set.issubset(fieldnames):
                    fieldnames.update(row_set)
                output_dicts.append(row)

with open("dataForImagesAndVideos.csv", "w", newline="") as f_output:
    writer = csv.DictWriter(f_output, fieldnames=list(fieldnames))
    writer.writeheader()
    for row in output_dicts:
        writer.writerow(row)