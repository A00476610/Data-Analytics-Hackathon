# src/transform.py
import re
import pandas as pd
from src.logger import log_progress
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

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
   mappings = {"bachelor/studio": 1}  # Expand with other direct mappings if needed

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

def clean_price_column(df):
    # Conversion with error handling
    try:
        df['price'] = pd.to_numeric(df['price'])
        # Fill empty cells with the mode value (most frequent value)
        mode_value = df['price'].mode().iloc[0]
        df['price'].fillna(mode_value, inplace=True)
    except ValueError:
        print()
        message = "Warning: Some values in the 'price' column could not be converted to numeric."
        log_progress(message)
        print (message)

    return df

# Clean the 'Size (sqft)' column
def clean_sqft(value):
    if value == "Not Available":
        return None
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

# Define a function to extract postal codes
def extract_postal_code(address):
    postal_code = re.findall(r'\b[A-Z]\d[A-Z] \d[A-Z]\d\b', address)
    if postal_code:
        return postal_code[0]
    else:
        return None

def clean_move_in_date(df):
    try:
        df['move_in_date'] = pd.to_datetime(df['move_in_date'], errors='coerce')  # Convert to datetime
        df['move_in_date'] = df['move_in_date'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Format
        df['move_in_date'] = df['move_in_date'].interpolate('linear')  # Interpolate missing dates 
        df['move_in_date'] = df['move_in_date'].fillna(method='bfill')
        df['move_in_date'] = pd.to_datetime(df['move_in_date'], errors='coerce')
        return df

    except ValueError as e:
        message = f"Error encountered during date conversion: {e}"
        log_progress(message)
        print(message)
        return df  # Return the DataFrame with potential errors

# Function to handle the geocoding
def geocode_address(location):
    geolocator = Nominatim(user_agent="rental_app")
    try:
        return geolocator.geocode(location, timeout=10)
    except GeocoderTimedOut:
        return geocode_address(location)
    except GeocoderUnavailable:
        return None
    
def transform(df):
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

#-------- Extracting Apartments only
    # Filter for 'Apartment' rentals
    df = df[df['rental_type'] == 'Apartment']
        
#-------- Deleting company columns
    message = "Dropping column 'company'"
    log_progress(message)
    del df['company']
    message = "Dropping column 'elevator_accessibility_features'"
    log_progress(message)
    del df['elevator_accessibility_features']

#---------- Processing 'price'
    df = clean_price_column(df.copy())

    # Map int to cleaning functions
    apply_cols = {
        # 'price': clean_price_column,
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
    # Apply the function to your DataFrame
    df = clean_move_in_date(df.copy()) 
    
    print('move_in_date', ": ", df['move_in_date'].dtype, df['move_in_date'].count())
    
    # # Apply the function to the 'address' column and create a new column 'postal_code'
    df['postal_code'] = df['address'].apply(extract_postal_code)
    print('postal_code', ": ", df['postal_code'].dtype, df['postal_code'].count())
    
    # # Calculate rate per square foot
    df['rate_per_sqft'] = df['price'] / df['size_sqft']

    # # Round rate_per_sqft to 2 decimal places
    df['rate_per_sqft'] = df['rate_per_sqft'].round(2)
    print('rate_per_sqft', ": ", df['rate_per_sqft'].dtype, df['rate_per_sqft'].count())

#---------- Clean Move In Date Column
    if 'address' in df.columns:
		# Apply geolocation to each address and store the result in the original DataFrame
        df['location'] = df['address'].apply(geocode_address)

		# Extract latitude and longitude, checking for None
        df['lat'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
        df['long'] = df['location'].apply(lambda loc: loc.longitude if loc else None)
    else:
        message = "The 'address' column does not exist in the CSV."
        log_progress(message)
        print(message)
    return df