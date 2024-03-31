import sys, os

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halifax_rental_hackathon.settings")
import django
import seaborn as sns
import plotly.express as px
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from joblib import load, dump
import shap

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

from sklearn.preprocessing import LabelEncoder
django.setup()

import pandas as pd
from django_pandas.io import read_frame
from llm_core.models import Apartment, Location, Amenities
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import randint, uniform


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
df.drop(['id', 'amenities', 'predicted_price', 'location', 'amenities__id', 'amenities__apartment', 'location__address', 'region', 'postal_code', 'rental_type', 'title', 'move_in_date', 'date_posted', 'agreement_type'], axis=1, inplace=True)

#
# # check null values
# df.info()
# df.dropna(inplace=True)  # drop null values
# df.info()


# Dividing data in input/output dataframes, X as input and Y as output
x_data = df.drop(['price'], axis=1)
y_data = df['price']

# splitting data in train test 80% and 20%
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)

# joining training data in one dataset
train_data = x_train.join(y_train)

# Generating Histogram for Distribution of multiple features
# train_data.hist(figsize=(15, 10))


# gaussian bell curve
train_data['days_until_move_in'] = np.log(train_data['days_until_move_in'] + 1)
#
# # Generating Histogram for Distribution of multiple features
# train_data.hist(figsize=(15, 10))
#
# # plot heatmap of correlation values
# plt.figure(figsize=(15,10))
# sns.heatmap(train_data.corr(), annot=True, cmap="YlGnBu", fmt=".2f", annot_kws={"size": 8})
#
#
# # plotting price on map w.r.t longitude and latitude
# plt.figure(figsize=(15, 8))
# sns.scatterplot(x="lat",y="long", data=train_data, hue="price", palette="coolwarm")
#
#
# # Exclude amenities column for pairplot only
# exclude_columns = [col for col in train_data.columns if 'amenities__' in col]
# include_columns = train_data.columns.difference(exclude_columns)
# plt.figure(figsize=(15,10))
# sns.pairplot(train_data[include_columns])


# scores of both models
forest_test_score = 0
xgb_test_score = 0

# Random forest without HyperParameter tunning
forest_model = RandomForestRegressor()
forest_model.fit(x_train, y_train)
forest_model.score(x_test, y_test)  # 0.738

forest_model_filename = 'best_forest_model.joblib'


# Check if the model file exists
if os.path.exists(forest_model_filename):
    # Load the existing model
    forest_model = load(forest_model_filename)
    print("Model loaded from file.")
else:
    # Hyperparameter tunning for better performance
    param_grid = {
        "n_estimators": [200, 300, 500],
        "max_features": [30, 40, 50],
        "min_samples_split": [4, 6, 8, 10],
        "max_depth": [None, 4, 8]
    }
    grid_search = GridSearchCV(forest_model, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True)

    grid_search.fit(x_train, y_train)
    forest_model = grid_search.best_estimator_
    forest_test_score = forest_model.score(x_test, y_test)
    dump(forest_model, forest_model_filename)


# XGBoost for Model Training
xgb_model = XGBRegressor()
xgb_model.fit(x_train, y_train)
xgb_model.score(x_test, y_test)  # 75 percent


# XGBoost Greedy Gradient Booster Regressor with Fine Tunning
xgb_model_filename = 'best_xgb_model.joblib'

# Check if the model file exists
if os.path.exists(xgb_model_filename):
    # Load the existing model
    xgb_model = load(xgb_model_filename)
    print("Model loaded from file.")
else:

    # Define the parameter distributions for hyper parameter tunning
    param_dist = {
        'n_estimators': randint(50, 500),
        'max_depth': randint(3, 10),
        'learning_rate': uniform(0.01, 0.2),  # continuous distribution from 0.01 to 0.21
        'colsample_bytree': uniform(0.5, 0.5),  # continuous distribution from 0.5 to 1.0
    }

    # Initialize RandomizedSearchCV
    random_search = RandomizedSearchCV(
        estimator=xgb_model,
        param_distributions=param_dist,
        n_iter=100,  # Number of parameter settings sampled
        scoring='neg_mean_squared_error',
        cv=3,  # Number of folds in cross-validation
        verbose=1,
        random_state=42,  # For reproducibility
        n_jobs=-1  # Use all available cores
    )

    # Fit RandomizedSearchCV
    random_search.fit(x_train, y_train)
    # Best estimator found by RandomizedSearchCV
    xgb_model = random_search.best_estimator_
    # Save the model to a file
    xgb_model_filename = 'best_xgb_model.joblib'
    dump(xgb_model, xgb_model_filename)


# Testing on both models

forest_test_score = forest_model.score(x_test, y_test)
print(f"Best score on Random Forest test dataset: {forest_test_score}")


xgb_test_score = xgb_model.score(x_test, y_test)
print(f"Best score on XGBoost Gradient Booster test dataset: {xgb_test_score}")


predicted_prices = xgb_model.predict(x_data)  # Example using XGBoost model

print(len(predicted_prices))
print(len(df))


for index, apartment in enumerate(Apartment.objects.all()):
    apartment.predicted_price = predicted_prices[index]
    apartment.save()

print(apartment)


#
#
#
#
# # Assuming initial scores before tuning
# initial_forest_score = 0.738  # Example initial score for Random Forest
# initial_xgb_score = 0.75  # Example initial score for XGBoost
#
# # Scores after hyperparameter tuning
# # Assume these are the scores you obtained after tuning
# tuned_forest_score = forest_test_score
# tuned_xgb_score = xgb_test_score
#
# # Names of models
# models = ['Random Forest', 'XGBoost']
#
# # Scores before tuning
# initial_scores = [initial_forest_score, initial_xgb_score]
#
# # Scores after tuning
# tuned_scores = [tuned_forest_score, tuned_xgb_score]
#
# # Set up the bar width
# barWidth = 0.3
#
# # Set position of bar on X axis
# r1 = np.arange(len(models))
# r2 = [x + barWidth for x in r1]
#
# # Make the plot
# plt.figure(figsize=(10, 6))
# plt.bar(r1, initial_scores, color='skyblue', width=barWidth, edgecolor='grey', label='Initial')
# plt.bar(r2, tuned_scores, color='lightgreen', width=barWidth, edgecolor='grey', label='Tuned')
#
# # Add xticks on the middle of the group bars
# plt.xlabel('Model', fontweight='bold')
# plt.xticks([r + barWidth for r in range(len(models))], models)
# plt.ylabel('Test Score (R^2)')
# plt.title('Model Performance: Initial vs. Tuned')
#
# # Create legend & Show graphic
# plt.legend()
# plt.show()
#
#
#
#
#
# # comparison between accuracy of two models
#
# # Names of models
# models = ['Random Forest', 'XGBoost']
#
# forest_test_score = 0.83
# xgb_test_score = 0.91
# # Test scores
# scores = [forest_test_score, xgb_test_score]
#
# # Create bar plot
# plt.figure(figsize=(10, 6))
# plt.bar(models, scores, color=['skyblue', 'blue'])
#
# # Adding title and labels
# plt.title('Model Performance Comparison')
# plt.ylabel('Test Score (R^2)')
# plt.ylim(min(scores) - 0.05, max(scores) + 0.05)  # Adjusting limits for better visualization
# plt.grid(axis='y', linestyle='--')
#
# # Display the plot
# plt.show()
#
#
# # residual plots
#
# plt.figure(figsize=(14, 6))
#
# # Random Forest residuals
# plt.subplot(1, 2, 1)
# sns.residplot(x=y_test, y=forest_model.predict(x_test), lowess=True, line_kws={'color': 'red', 'lw': 1})
# plt.title('Random Forest Residuals')
# plt.xlabel('Observed Values')
# plt.ylabel('Residuals')
#
# # XGBoost residuals
# plt.subplot(1, 2, 2)
# sns.residplot(x=y_test, y=xgb_model.predict(x_test), lowess=True, line_kws={'color': 'red', 'lw': 1})
# plt.title('XGBoost Residuals')
# plt.xlabel('Observed Values')
# plt.ylabel('Residuals')
#
# plt.tight_layout()
# plt.show()
#
#
# # Prediction Error Plots
# plt.figure(figsize=(14, 6))
#
# # Random Forest
# plt.subplot(1, 2, 1)
# plt.scatter(y_test, forest_model.predict(x_test), alpha=0.3)
# plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
# plt.title('Random Forest Prediction Error')
# plt.xlabel('True Value')
# plt.ylabel('Predicted Value')
#
# # XGBoost
# plt.subplot(1, 2, 2)
# plt.scatter(y_test, xgb_model.predict(x_test), alpha=0.3)
# plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
# plt.title('XGBoost Prediction Error')
# plt.xlabel('True Value')
# plt.ylabel('Predicted Value')
#
# plt.tight_layout()
# plt.show()
#
#
# # checking feature importance in random forest
#
# # Calculate SHAP values for the Random Forest model
# explainer = shap.TreeExplainer(forest_model)
# shap_values = explainer.shap_values(x_train.iloc[:100])
#
# shap.summary_plot(shap_values, x_train.iloc[:100], plot_type="bar")
#
#
# # Random Forest Feature Importance
# forest_importances = pd.Series(forest_model.feature_importances_, index=x_train.columns)
# forest_importances_sorted = forest_importances.sort_values(ascending=False)
#
# # XGBoost Feature Importance
# xgb_importances = pd.Series(xgb_model.feature_importances_, index=x_train.columns)
# xgb_importances_sorted = xgb_importances.sort_values(ascending=False)
#
# # Plotting
# plt.figure(figsize=(14, 7))
#
# plt.subplot(1, 2, 1)
# forest_importances_sorted.head(10).plot(kind='barh', title='Top 10 Features in Random Forest', color='skyblue').invert_yaxis()  # invert_yaxis for descending order
# plt.xlabel('Feature Importance')
#
# plt.subplot(1, 2, 2)
# xgb_importances_sorted.head(10).plot(kind='barh', title='Top 10 Features in XGBoost', color='lightgreen').invert_yaxis()
# plt.xlabel('Feature Importance')
#
# plt.tight_layout()
# plt.show()


df.to_csv("halifax_rental_apartment_data.csv", index=False)



