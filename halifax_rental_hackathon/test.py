import sys, os

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halifax_rental_hackathon.settings")
import django
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
django.setup()

import pandas as pd
from django_pandas.io import read_frame
from llm_core.models import Apartment, Location, Amenities
from sklearn.model_selection import GridSearchCV


# Query the data and create the DataFrame
qs = Apartment.objects.select_related('location', 'amenities')
fieldnames = [field.name for field in Apartment._meta.get_fields()]
fieldnames.extend([
    'location__address',  # Include the 'address' field from the Location model
    *[f'amenities__{field.name}' for field in Amenities._meta.get_fields()]
])
df = read_frame(qs, fieldnames=fieldnames)


# one hot encoding for categorical values
label_encoder = LabelEncoder()
df['agreement_type_encoded'] = label_encoder.fit_transform(df['agreement_type'])


# creating a new feature, number of days left for moving in house
df['days_until_move_in'] = (df['move_in_date'] - df['date_posted']).dt.days

# in case of negative move in days value, replacing it with median
median_days_until_move_in = df[df['days_until_move_in'] > 0]['days_until_move_in'].median()
df.loc[df['days_until_move_in'] < 0, 'days_until_move_in'] = median_days_until_move_in


# converting long/latitude in numbers
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['long'] = pd.to_numeric(df['long'], errors='coerce')
df['size_sqft'] = pd.to_numeric(df['size_sqft'], errors='coerce')


# transforming pet friendly column
df['amenities__pet_friendly'] = df['amenities__pet_friendly'].apply(lambda x: x.lower() in ['yes', 'limited'])



# 'amenities__pet_friendly', 'amenities__smoking_permitted',
#                   'amenities__barrier_free_entrances_ramps', 'amenities__visual_aids',
#                   'amenities__accessible_washrooms_in_suite'

cols_to_convert = ['amenities__pet_friendly', 'amenities__smoking_permitted',
                   'amenities__barrier_free_entrances_ramps', 'amenities__visual_aids',
                   'amenities__accessible_washrooms_in_suite']

# Convert to 'True' only if the value is the string "True" (case-insensitive), else 'False'
df[cols_to_convert] = df[cols_to_convert].applymap(lambda x: str(x).strip().lower() == 'true')



# removing unnecessary columns
df.drop(['id', 'amenities', 'location', 'amenities__id', 'amenities__apartment', 'location__address', 'region', 'postal_code', 'rental_type', 'title', 'move_in_date', 'date_posted', 'agreement_type'], axis=1, inplace=True)


# check null values
df.info()
df.dropna(inplace=True)  # drop null values
df.info()


# Dividing data in input/output dataframes, X as input and Y as output
x_data = df.drop(['price'], axis=1)
y_data = df['price']

# splitting data in train test 80% and 20%
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)

# joining training data in one dataset
train_data = x_train.join(y_train)

# Generating Histogram for Distribution of multiple features
train_data.hist(figsize=(15, 10))


# gaussian bell curve
train_data['days_until_move_in'] = np.log(train_data['days_until_move_in'] + 1)
#
#
# # Generating Histogram for Distribution of multiple features
# train_data.hist(figsize=(15, 10))
#
# # plot heatmap of correlation values
# plt.figure(figsize=(15,10))
# sns.heatmap(train_data.corr(), annot=True, cmap="YlGnBu", fmt=".2f", annot_kws={"size": 8})
#
#
# plotting price on map w.r.t longitude and latitude
# plt.figure(figsize=(15, 8))
# sns.scatterplot(x="lat",y="long", data=train_data, hue="price", palette="coolwarm")


# Random Forest Model Training
forest = RandomForestRegressor()
forest.fit(x_train, y_train)
forest.score(x_test, y_test)  # 0.738


# Hyperparameter tunning for better performance
param_grid = {
    "n_estimators": [200, 300, 500],
    "max_features": [30, 40, 50],
    "min_samples_split": [4, 6, 8, 10],
    "max_depth": [None, 4, 8]
}
grid_search = GridSearchCV(forest, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True)

grid_search.fit(x_train, y_train)
best_forest = grid_search.best_estimator_
best_forest.score(x_test, y_test)
print(best_forest.score(x_test, y_test))

df.to_csv("halifax_rental_apartment_data.csv", index=False)
print(df.head())




