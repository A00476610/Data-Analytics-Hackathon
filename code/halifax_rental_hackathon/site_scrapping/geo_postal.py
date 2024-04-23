import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="rental_app")

postal_code_to_region = {
    'B3H': 'South End Halifax',
    'B3J': 'Downtown Halifax',
    'B3K': 'North End Halifax',
    'B3M': 'Clayton Park',
    'B3L': 'West End of Halifax',
    'B3N': 'Fairview Halifax',
    'B3S': 'Bayers Lake Halifax',
    'B3P': 'Cowie Hill',
    'B3R': 'Spryfield Halifax',
    'B3Z': 'coastal communities around Halifax',
    'B4B': 'Bedford Halifax',
    'B4E': 'Sackville'
}

# Function to handle the geocoding
def geocode_address(location):
    try:
        return geolocator.geocode(location, timeout=10)
    except GeocoderTimedOut:
        return geocode_address(location)
    except GeocoderUnavailable:
        return None
    
def get_region_from_postal_code(postal_code):
    if pd.isnull(postal_code) or len(postal_code) < 3:
        return "Unknown"
    return postal_code_to_region.get(postal_code[:3], "Unknown")

# Load the CSV file
real_estate_data = pd.read_csv('real_estate_data.csv')

# Ensure the 'address' column exists
if 'address' in real_estate_data.columns:
    # Apply geolocation to each address and store the result in the original DataFrame
    real_estate_data['location'] = real_estate_data['address'].apply(geocode_address)

    # Extract latitude and longitude, checking for None
    real_estate_data['lat'] = real_estate_data['location'].apply(lambda loc: loc.latitude if loc else None)
    real_estate_data['long'] = real_estate_data['location'].apply(lambda loc: loc.longitude if loc else None)

    # Optionally, you can drop the 'location' column if it's no longer needed
    real_estate_data = real_estate_data.drop('location', axis=1)

    # Save the updated DataFrame to a new CSV file
    real_estate_data.to_csv('updated_real_estate_data.csv', index=False)
else:
    print("The 'address' column does not exist in the CSV.")
