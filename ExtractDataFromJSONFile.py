import json  
import csv  

'''read image url and image metadata from the json file downloaded 
from AWS
'''
with open('/Users/wusongyuan/Desktop/Downloads/projects.json') as f_input, open("dataForImagesAndVideos.csv", "w", newline="") as f_output:
    json_data = json.load(f_input, strict = False)
    """Convert json file to csv file"""
    items_list = json_data['Items']
    '''check whether it is python dict'''
    print(type(items_list))
    '''Storing uesful keys and values'''
    empty_dict = {}
    '''Storing columns names'''
    fieldnames = []
    count = 0
    for entry in items_list:
        if 'scenes' in entry.keys():
            inner_list = entry['scenes']['L']
            for element in inner_list:
                empty_dict['image'] = element['M']['image']
                if 'imageMetadata' in element['M'].keys():
                        map3 = json.loads(element['M']['imageMetadata']['S'])
                        for key in map3.keys():
                            empty_dict.update({key:map3[key]})
                        fieldnames.extend(empty_dict.keys())
                        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
                        if count == 0:
                            writer.writeheader()
                            count += 1
                        writer.writerow(empty_dict)
                        empty_dict.clear()

