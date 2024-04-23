import pandas as pd

# Load the real estate data
real_estate_data = pd.read_csv('clean_long_term_rental_kijiji.csv')

# Define the mapping of postal code prefixes to regions
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
    # Add other mappings as necessary
}

# Function to determine the region based on address, location, and postal code
def get_region(row):
    address = row['address'].lower() if pd.notnull(row['address']) else ''
    location = row['location'].lower() if pd.notnull(row['location']) else ''

    # Check if specific areas are mentioned in the address or location
    if 'downtown' in address or 'downtown' in location:
        return 'Downtown Halifax'
    if 'south end' in address or 'south end' in location:
        return 'South End Halifax'
    if 'clayton park' in address or 'clayton park' in location:
        return 'Clayton Park'
    if 'west end' in address or 'west end' in location:
        return 'West End of Halifax'
    if 'north end' in address or 'north end' in location:
        return 'North End Halifax'
    if 'fairview' in address or 'fairview' in location:
        return 'Fairview Halifax'

    # If no specific area is mentioned, use the postal code to determine the region
    postal_code = row['postal_code']
    if pd.isnull(postal_code) or len(postal_code) < 3:
        return "Unknown"
    return postal_code_to_region.get(postal_code[:3], "Unknown")

# Apply the function to each row to create a new Region column
real_estate_data['Region'] = real_estate_data.apply(get_region, axis=1)

# Save the updated DataFrame to a CSV file
real_estate_data.to_csv('updated_real_estate_data.csv', index=False)
