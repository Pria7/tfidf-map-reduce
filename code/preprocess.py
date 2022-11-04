import pandas as pd
import numpy as np
from sklearn import preprocessing
import os

# feature engineering
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

toys = pd.read_json('/kaggle/input/amazon-product-review-spam-and-non-spam/Toys_and_Games/Toys_and_Games.json', lines=True)

# remove redundant columns
toys_df = toys.drop(['unixReviewTime', 'asin'], axis=1)
toys = []
toys_df = toys_df.dropna(subset=['class'])
# toys_df

# normalize and scale the overall column (product rating)
# x = toys_df['overall']
# x = x.values.reshape(-1,1) 
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# toys_df['overall'] = pd.DataFrame(x_scaled)
toys_df = toys_df.rename(columns={"overall": "rating", "helpful" : "votes-down/up"})
# toys_df['reviewText'] = toys_df['reviewText'].astype('str')

# id column cleanup
toys_df = toys_df.rename(columns={"_id": "id"})
toys_df['id'] = toys_df['id'].dropna()
toys_df['id'] = toys_df['id'].astype('str')
toys_df['id'] = toys_df['id'].str.split(' ').str[1].str.replace('}', '').str[1:-1]

# review time column cleanup
toys_df['reviewTime'] = toys_df['reviewTime'].str.replace(',', '').str.replace(' ', '.')

# text columns cleanup
toys_df['reviewText'] = toys_df['reviewText'].str.lower().str.replace('[^\w\s]', '')
toys_df = toys_df.loc[toys_df['reviewText'].str.len() > 90] # average length of the sentace is 20-25 words at 4.7 chars per word hence 90 characters or below is filtered

toys_df

new_df = toys_df[['reviewerID', 'reviewText', 'class']]

new_df['reviewText'] = new_df['reviewText'].str.replace('[^0-9a-zA-Z\s]', ' ')

new_df.to_csv('final_data.csv', sep='|', index = False)