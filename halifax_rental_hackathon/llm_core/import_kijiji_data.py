import csv
import django

django.setup()
from llm_core.models import Apartment, Amenities, Location  # Replace 'your_app' with your Django app name

with open('D:/hackathon/Data-Analytics-Hackathon/halifax_rental_hackathon/llm_core/updated_real_estate_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = Location(
            address=row.get('address', ''),  # Fill missing 'title' with empty string
        )
        location.save()
        # try:
        amenities = Amenities(
            num_parking = float(row.get('num_parking',0)),
            pet_friendly = row['pet_friendly'],
            furnished = row['furnished'],
            air_conditioning = row['air_conditioning'],
            smoking_permitted = row['smoking_permitted'],
            barrier_free_entrances_ramps = row['barrier_free_entrances_ramps'],
            visual_aids = row['visual_aids'],
            accessible_washrooms_in_suite = row['accessible_washrooms_in_suite'],
            heat = row['heat'],
            hydro = row['hydro'],
            water = row['water'],
            cable_tv = row['cable_tv'],
            internet = row['internet'],
            laundry_unit = row['laundry_unit'],
            laundry_building = row['laundry_building'],
            dishwasher = row['dishwasher'],
            fridge_freezer = row['fridge_freezer'],
            yard = row['yard'],
            balcony = row['balcony'],
            building_security = row['building_security'],
            building_elevator = row['building_elevator'],
            building_gym = row['building_gym'],
            bycycle_parking = row['bycycle_parking'],
            storage_space = row['storage_space'],
        )
        amenities.save()
        # except django.core.exceptions.ValidationError as e:
        #     print(f"Error in row: {row} - Validation Error: {e}") 
        # try:
        apartment = Apartment(
            location=location, 
            title=row.get('title', ''),  # Fill missing 'title' with empty string
            rental_type=row['rental_type'],
            price=float(row.get('price', 0.0)),  # Fill missing 'price' with 0.0 
            date_posted = row['date_posted'], # Fill missing 'date_posted'
            move_in_date = row['move_in_date'], # Fill missing 'move_in
            agreement_type=row['agreement_type'],
            num_bedrooms=float(row.get('num_bedrooms', 0)),  # Fill missing with 0
            num_bathrooms=float(row.get('num_bathrooms', 0)),  # Fill missing with 0
            size_sqft=(row.get('size_sqft', 0)),  # Fill missing with 0
            postal_code = row['postal_code'],
            rate_per_sqft = row['rate_per_sqft'],
            lat = row['lat'], 
            long = row['long'],
            region = row['Region'],
            amenities = amenities,
        )
        apartment.save()
        # except django.core.exceptions.ValidationError as e:
        #     print(f"Error in row: {row} - Validation Error: {e}") 