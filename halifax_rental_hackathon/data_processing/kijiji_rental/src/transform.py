# src/transform.py
import pandas as pd
from src.logger import log_progress

# Clean the 'Parking Included' column
def clean_parking(value):
    try:
        # Remove any leading '+' sign and convert to integer
        value = str(value).strip('+')  
        return float(value)
    except ValueError:
        message = "Warning: Some values in the 'num_parking' could not be converted to numbers:" + str(value)
        log_progress(message)
        print (message)
        return float('nan')  # Replace with NaN


def clean_bedroom_data(col):
   mappings = {"bachelor/studio": 0}  # Expand with other direct mappings if needed

   col = col.str.lower() 
   col.replace(mappings, inplace=True)

   def _clean(value): 
        if isinstance(value, str):
            value = value.split()[0]  # Split on space, take the first part
            value = value.strip('+')  # Remove any trailing '+'
            try:
                return float(value)
            # Strip the number and return the rest
            except ValueError:
                message = "Warning: Some values in the 'num_bedroom' could not be converted to numbers:" + str(ValueError)
                log_progress(message)
                print (message)
            return ''
        return value  # If not a string or no leading number, return as is

   col = col.apply(_clean)
   mode_value = col.mode()[0]
   col.fillna(mode_value, inplace=True)
   return col

# Clean the 'Size (sqft)' column
def clean_price(value):
    try:
        value = str(value).replace(',', '')
        value = value.replace('.', '')
        return float(value)
    except ValueError:
        message = "Warning: Some values in the 'price' could not be converted to numbers:" + str(value)
        log_progress(message)
        print (message)
        return float('nan')  # Replace with NaN for better handling

# Clean the 'Size (sqft)' column
def clean_sqft(value):
    if value == "Not Available":
        return value
    else:
        try:
            return float(str(value).replace(',', ''))
        except ValueError:
            message = "Warning: Some values in the 'size_sqft' could not be converted to numbers:" + str(ValueError)
            log_progress(message)
            print (message)
            return float('nan')  # Replace with NaN for better handling

def clean_helper_apply(col, clean_fn):
    col = col.apply(clean_fn)
    # Fill empty cells with the mode value (most frequent value)
    mode_value = col.mode().iloc[0]
    col.fillna(mode_value, inplace=True)
    return col

def clean_helper_fillna(col):
    # Fill empty cells with the mode value (most frequent value)
    mode_value = col.mode().iloc[0]
    col.fillna(mode_value, inplace=True)
    return col

def convert_yes_no_to_bool(df, columns):
  for col in columns:
    # Convert to lowercase for case-insensitive comparison
    df[col] = df[col].str.lower()

    # Convert 'yes' to True, 'no' and 'not available' to False
    df[col].replace({'yes': True, 'no': False, 'not available': False}, inplace=True)
  return df

def transform(df):
    
#-------- Deleting company columns
    message = "Dropping column 'company'"
    log_progress(message)
    del df['company']
    message = "Dropping column 'elevator_accessibility_features'"
    log_progress(message)
    del df['elevator_accessibility_features']

    # Map int to cleaning functions
    apply_cols = {
        'price': clean_price,
        'num_parking': clean_parking,
        'size_sqft': clean_sqft,
    }
    fillna_cols_2 = [
        'furnished',
        'air_conditioning',
        'smoking_permitted',
        'barrier_free_entrances_ramps',
        'visual_aids',
        'accessible_washrooms_in_suite',
        'heat', 'hydro', 'water', 'cable_tv', 'internet', 'laundry_unit', 'laundry_building', 'dishwasher', 'fridge_freezer', 'yard', 'balcony', 'building_security', 'building_elevator', 'building_gym', 'bycycle_parking', 'storage_space'
    ]
    fillna_cols = [
        'rental_type',
        'num_bathrooms',
        'agreement_type', 
        'pet_friendly',
        *fillna_cols_2,    ]
    # Generalized cleaning loop for columns using "apply"
    for col, cleaner_func in apply_cols.items(): 
        print(col, ": ", df[col].dtype, df[col].count())
        df[col] = clean_helper_apply(df[col], cleaner_func)
        print(col, ": ", df[col].dtype, df[col].count())

    # Generalized cleaning loop for columns using pnly fillna
    for col in fillna_cols: 
        print(col, ": ", df[col].dtype, df[col].count())
        print(col, df[col].unique())
        df[col] = clean_helper_fillna(df[col])
        print(col, ": ", df[col].dtype, df[col].count())
        print(col, df[col].unique())
        # Generalized cleaning loop for columns using pnly fillna
    
    df = convert_yes_no_to_bool(df, fillna_cols_2)
    
#----------- Clean Address

#----------- Clean num_bedroom column
    print('num_bedrooms', df['num_bedrooms'].unique())
    print('num_bedrooms', ": ", df['num_bedrooms'].dtype, df['num_bedrooms'].count())
    df['num_bedrooms'] = clean_bedroom_data(df['num_bedrooms'])
    print('num_bedrooms', df['num_bedrooms'].unique())
    print('num_bedrooms', ": ", df['num_bedrooms'].dtype, df['num_bedrooms'].count())

#---------- Clean Date Posted column
    # Convert date column to datetime
    print('date_posted', ": ", df['date_posted'].dtype, df['date_posted'].count())
    try:
        df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')  # 'coerce' handles bad values
        # Interpolate AND assign back to the column
        df['date_posted'] = df['date_posted'].interpolate(method='linear')
    except ValueError:
        message = "Warning: Some values in the date_posted could not be converted to numbers:" + str(ValueError)
        log_progress(message)
        print (message)
    print('date_posted', ": ", df['date_posted'].dtype, df['date_posted'].count())

#---------- Clean Move In Date Column
    # Convert move_in column to datetime
    print('move_in_date', ": ", df['move_in_date'].dtype, df['move_in_date'].count())
    try:
        df['move_in_date'] = pd.to_datetime(df['move_in_date'], format='%d-%b-%y') 
        # Interpolate AND assign back to the column
        df['move_in_date'] = df['move_in_date'].interpolate(method='linear')
    except ValueError:
        message = "Warning: Some values in the move_in_date could not be converted to numbers:" + str(ValueError)
        log_progress(message)
        print (message)
    print('move_in_date', ": ", df['move_in_date'].dtype, df['move_in_date'].count())
    
    return df