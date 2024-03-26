import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="rental_app")

# Function to handle the geocoding
def geocode_address(location):
    try:
        return geolocator.geocode(location, timeout=10)
    except GeocoderTimedOut:
        return geocode_address(location)
    except GeocoderUnavailable:
        return None

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

    # Display the updated DataFrame
    print(real_estate_data.head())

    # Save the updated DataFrame to a new CSV file
    real_estate_data.to_csv('updated_real_estate_data.csv', index=False)
else:
    print("The 'address' column does not exist in the CSV.")
