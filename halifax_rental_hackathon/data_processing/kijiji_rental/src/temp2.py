# src/transform.py
import pandas as pd
from src.logger import log_progress


def clean_date_data(value):
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):  # Add more formats as needed
            try:
                return pd.to_datetime(value, format=fmt)
            except ValueError:
                pass  # Try the next format 
        print(f"Warning: Could not convert date: {value}") 
        return pd.NaT  # Or another suitable default 
    else:
        return value


# Define cleaning functions
def clean_parking_data(value):
    if isinstance(value, str):
        try:
            value = value.strip('+') 
            return int(value) 
        except ValueError:
            message = "Warning: Some values in the Parking Included could not be converted to numbers:" + str(value)
            log_progress(message)
            print (message)
            return None
    else:
        return value  


def clean_bedroom_data(value):
    if isinstance(value, str):
        if value.lower() == "bachelor/studio":
            return 0
        else:
            value = value.split()[0]  # Split on space, take the first part
            value = value.strip('+')  # Remove any trailing '+'
            try:
                return int(value)
            except ValueError:
                message = "Warning: Some values in the Bedroom could not be converted to numbers: "
                log_progress(message)
                print (message)
                return None
    else:
        return value


def clean_price_data(value):
    if isinstance(value, str):
        try:
            value = value.rstrip('.').replace(',', '')  # Remove commas
            return int(float(value))  
        except ValueError:
            message = "Warning: Some values in the Price could not be converted to numbers:" + str(value)
            log_progress(message)
            print (message)
            return None
    else:
        return value  
    
def clean_size_data(value):
    if isinstance(value, str):
        value = value.replace(',', '')  # Remove commas
        if value.lower() == 'not available':
            return pd.NA  # Or another suitable default for missing data
        else:
            try:
                return int(value)
            except ValueError:
                message = "Warning: Some values in the Price could not be converted to numbers:" + str(value)
                log_progress(message)
                print (message)
                return pd.NA 
    else:
        return value
    
def convert_yes_no_to_bool(df, columns):
  for col in columns:
    # Convert to lowercase for case-insensitive comparison
    df[col] = df[col].str.lower()

    # Convert 'yes' to True, 'no' and 'not available' to False
    df[col].replace({'yes': True, 'no': False, 'not available': False}, inplace=True)

    # Fill empty cells with False
    df[col].fillna(False, inplace=True)
  return df


def transform(df):
    # Map int to cleaning functions
    int_column_cleaners = {
        'parking_included': clean_parking_data,
        'num_bedrooms': clean_bedroom_data,
        'price': clean_price_data,
        'size_sqft': clean_size_data,
    }
    print ('parking_included: ', df['parking_included'].unique())

    # Generalized cleaning and conversion loop to int
    for col, cleaner_func in int_column_cleaners.items(): 
        print(col, ": ", df[col].dtype, df[col].count())
        try:
            df[col] = pd.to_numeric(df[col]) 
        except ValueError:
            df[col] = df[col].apply(cleaner_func)
        print(col, ": ", df[col].dtype, df[col].count())
    
    print ('--------------------parking_included: ', df['parking_included'].unique())
    
    # Convert date column to datetime
    print('date_posted', ": ", df['date_posted'].dtype, df['date_posted'].count())
    try:
        df['date_posted'] = pd.to_datetime(df['date_posted'])
    except ValueError:
        message = "Warning: Some values in the date_posted could not be converted to numbers:" + str(value)
        log_progress(message)
        print (message)
    print('date_posted', ": ", df['date_posted'].dtype, df['date_posted'].count())


    # Convert move_in column to datetime
    print('move_in_date', ": ", df['move_in_date'].dtype, df['move_in_date'].count())
    try:
        df['move_in_date'] = pd.to_datetime(df['move_in_date'], format='%d-%b-%y') 
    except ValueError:
        message = "Warning: Some values in the move_in_date could not be converted to numbers:" + str(value)
        log_progress(message)
        print (message)
    print('move_in_date', ": ", df['move_in_date'].dtype, df['move_in_date'].count())

    # convert 
    # To check which columns needs cleaning
    print ("Printing unique values of columns: ")
    print ('rental_type: ', df['rental_type'].unique())
    print ('agreement_type: ', df['agreement_type'].unique())
    print ('pet_friendly: ', df['pet_friendly'].unique())
    print ('smoking_permitted: ', df['smoking_permitted'].unique())
    print ('elevator_accessibility_features: ', df['elevator_accessibility_features'].unique())
    print("Dropping empty column elevator_accessibility_features")
    del df['elevator_accessibility_features']


    print("\nBoolean columns")
    
    # Convert Yes No cols to Boolean
    columns_to_convert = ['furnished', 'air_conditioning', 'barrier_free_entrances_ramps', 'visual_aids', 'accessible_washrooms_in_suite', 'heat', 'hydro', 'water', 'cable_tv',  'internet', 'laundry_unit', 'laundry_building', 'dishwasher', 'fridge_freezer', 'yard', 'balcony', 'building_security', 'building_elevator', 'building_gym', 'bycycle_parking', 'storage_space']  # Replace with your actual column names
    df = convert_yes_no_to_bool(df, columns_to_convert)
    print ('furnished: ', df['furnished'].dtype, df['furnished'].unique())
    print ('air_conditioning: ', df['air_conditioning'].dtype, df['air_conditioning'].unique())
    print ('barrier_free_entrances_ramps: ', df['barrier_free_entrances_ramps'].dtype, df['barrier_free_entrances_ramps'].unique())
    print ('visual_aids: ', df['visual_aids'].dtype, df['visual_aids'].unique())
    print ('accessible_washrooms_in_suite: ', df['accessible_washrooms_in_suite'].dtype, df['accessible_washrooms_in_suite'].unique())
    print ('heat: ', df['heat'].dtype, df['heat'].unique())
    print ('hydro: ', df['hydro'].dtype, df['hydro'].unique())
    print ('water: ', df['water'].dtype, df['water'].unique())
    print ('cable_tv: ', df['cable_tv'].dtype, df['cable_tv'].unique())
    print ('internet: ', df['internet'].dtype, df['internet'].unique())
    print ('laundry_unit: ', df['laundry_unit'].dtype, df['laundry_unit'].unique())
    print ('laundry_building: ', df['laundry_building'].dtype, df['laundry_building'].unique())
    print ('dishwasher: ', df['dishwasher'].dtype, df['dishwasher'].unique())
    print ('fridge_freezer: ', df['fridge_freezer'].dtype,  df['fridge_freezer'].unique())
    print ('yard: ', df['yard'].dtype, df['yard'].unique())
    print ('balcony: ', df['balcony'].dtype, df['balcony'].unique())
    print ('building_security: ', df['building_security'].dtype, df['building_security'].unique())
    print ('building_elevator: ', df['building_elevator'].dtype, df['building_elevator'].unique())
    print ('building_gym: ', df['building_gym'].dtype, df['building_gym'].unique())
    print ('bycycle_parking: ', df['bycycle_parking'].dtype, df['bycycle_parking'].unique())
    print ('storage_space: ', df['storage_space'].dtype, df['storage_space'].unique())
    
    return df
          