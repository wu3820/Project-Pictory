import pandas as pd
import numpy as np

'''Remove duplicates in image-replaced event dataframe'''
col_names1 = ['client_event_time','new-image','project-id','old-image','source']
df1 = pd.read_csv('sample1.csv', usecols= col_names1, keep_default_na=False, na_values=[""]).drop_duplicates(keep='first')
df1['old-image'] = '\'' + df1['old-image'].astype(str) + '\''
df1['new-image'] = '\'' + df1['new-image'].astype(str) + '\''
df1.to_csv('outputFile_imageReplaced.csv', index = False)

'''Remove duplicates in asset-searched event datafreme'''
col_names2 = ['client_event_time','project-id','search-term','search-type']
df2 = pd.read_csv('sample2.csv', usecols= col_names2, keep_default_na=False, na_values=[""]).drop_duplicates(keep='first')
df2.to_csv('outputFile_assetSearched.csv', index = False)

'''Merge the image-replaced event dataframe with asset-searched event dataframe by inner join'''
merged_df = pd.merge(left = df1, right = df2, left_on = 'project-id', right_on = 'project-id').drop_duplicates(keep='first')
merged_df.to_csv('test_output1.csv', index = False)

'''Read data from csv file storing images and videos into one dataframe'''
df3 = pd.read_csv('dataForImagesAndVideos1.csv')
'''Check whether images in event dataframe also occured in previous dataframe'''
df3 = df3.assign(Label = merged_df['old-image'].isin(df3['image']).astype(str))

if df3['Label'].any() == 'False':
    df3['Label'] = 'Not Selected'
else:
    df3['Label'] = 'Selected'

'''Append the event dataframe into dataframe storing images and videos with label'''
merged_df = merged_df.rename(columns={'new-image':'image'})
merged_df['Label'] = pd.Series('Selected')
df4 = df3.append(merged_df,ignore_index=True)
df4.to_csv('test33334.csv')
df4 = pd.read_csv('test33334.csv', usecols = df3.columns, keep_default_na = False).drop_duplicates(keep='first')
df4.fillna(np.nan, inplace = True)
df4.to_csv('test32.csv') 
