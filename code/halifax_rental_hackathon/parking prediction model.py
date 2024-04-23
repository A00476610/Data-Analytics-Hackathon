import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halifax_rental_hackathon.settings")
import django
django.setup()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from django_pandas.io import read_frame
import numpy as np

# Assuming you've already set up Django environment
from llm_core.models import Parking

# Query your data
parkings = Parking.objects.all()
df = read_frame(parkings, fieldnames=[
    'type', 'available', 'price', 'tenant_services_coordinator',
    'resident_managers', 'commercial_property_manager', 'email',
    'website', 'tel', 'fax', 'term', 'termination_policy', 'deposit'
])

# Handle missing values (simple example: fill with median for numerical, mode for categorical)
df['price'] = df['price'].fillna(df['price'].median())
df['type'] = df['type'].fillna(df['type'].mode()[0])

# Convert 'available' to a numerical feature, e.g., days until available
df['available'] = pd.to_datetime(df['available']) - pd.to_datetime('now')
df['available'] = df['available'].dt.days

# Encode categorical variables
df = pd.get_dummies(df, drop_first=True)

# Split data into features and target
X = df.drop('price', axis=1)
y = df['price']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
