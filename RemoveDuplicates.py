import pandas as pd
'''Removing duplicates'''
used_cols = ['image','description','duration','id','keyword','large'
             ,'library','media_type','preview','preview_jpg','rank','thumb','thumb_jpg']
df = pd.read_csv('dataForImagesAndVideos.csv', usecols=used_cols).drop_duplicates(keep='first').reset_index()
df['image'] = df['image'].str[5:-1]
df.to_csv('dataForImagesAndVideos1.csv', index = False)
