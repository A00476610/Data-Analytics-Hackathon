import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halifax_rental_hackathon.settings")
import django
django.setup()
from llm_core.models import Amenities, Apartment, Location, TransformedAmenities

#
# def amenities_count():
#     """
#     This will store amenities count per apartment
#     Returns:
#
#     """
#     amenities = Amenities.objects.all()
#
#     for amenity in amenities:
#         # Calculate the sum of True values for boolean fields
#         true_count = sum([
#             # Boolean fields
#             amenity.furnished, amenity.air_conditioning, amenity.heat, amenity.hydro,
#             amenity.water, amenity.cable_tv, amenity.internet, amenity.laundry_unit,
#             amenity.laundry_building, amenity.dishwasher, amenity.fridge_freezer,
#             amenity.yard, amenity.balcony, amenity.building_security, amenity.building_elevator,
#             amenity.building_gym, amenity.bycycle_parking, amenity.storage_space,
#
#             # Non-boolean fields, check for 'Yes'
#             amenity.pet_friendly.lower() == 'yes',
#             amenity.smoking_permitted.lower() == 'true',
#             amenity.barrier_free_entrances_ramps.lower() == 'true',
#             amenity.visual_aids.lower() == 'true',
#             amenity.accessible_washrooms_in_suite.lower() == 'true'
#         ])
#
#         # Update amenities_count and save
#         amenity.amenities_count = true_count
#         amenity.save()
#
#
# amenities_count()











# import pandas as pd
# # Extract data from Apartment
# apartments_data = list(Apartment.objects.all().values())
# df_apartments = pd.DataFrame(apartments_data)
#
# # Extract data from Amenities
# amenities_data = list(Amenities.objects.all().values())
# df_amenities = pd.DataFrame(amenities_data)
#
# # Assuming 'amenities_id' is the foreign key in 'Apartment' that refers to 'Amenities'
# df_joined = pd.merge(df_apartments, df_amenities, left_on='amenities_id', right_on='id', how='left')
# print(df_joined)


def transform_amenities():
    amenities = Amenities.objects.all()

    for amenity in amenities:
        transformed = TransformedAmenities(
            num_parking=int(amenity.num_parking > 0),  # True if num_parking > 0, otherwise False
            pet_friendly=1 if amenity.pet_friendly == 'Yes' else 0,
            furnished=1 if amenity.furnished else 0,
            air_conditioning=1 if amenity.air_conditioning else 0,
            smoking_permitted=1 if amenity.smoking_permitted in ['Yes', 'outdoors only'] else 0,
            barrier_free_entrances_ramps=1 if amenity.barrier_free_entrances_ramps == 'Yes' else 0,
            visual_aids=1 if amenity.visual_aids == 'Yes' else 0,
            accessible_washrooms_in_suite=1 if amenity.accessible_washrooms_in_suite == 'Yes' else 0,
            heat=1 if amenity.heat else 0,
            hydro=1 if amenity.hydro else 0,
            water=1 if amenity.water else 0,
            cable_tv=1 if amenity.cable_tv else 0,
            internet=1 if amenity.internet else 0,
            laundry_unit=1 if amenity.laundry_unit else 0,
            laundry_building=1 if amenity.laundry_building else 0,
            dishwasher=1 if amenity.dishwasher else 0,
            fridge_freezer=1 if amenity.fridge_freezer else 0,
            yard=1 if amenity.yard else 0,
            balcony=1 if amenity.balcony else 0,
            building_security=1 if amenity.building_security else 0,
            building_elevator=1 if amenity.building_elevator else 0,
            building_gym=1 if amenity.building_gym else 0,
            bycycle_parking=1 if amenity.bycycle_parking else 0,
            storage_space=1 if amenity.storage_space else 0,
            amenities_count=amenity.amenities_count  # Assuming this is already an integer
        )
        transformed.save()

# Run the function to populate the transformed_amenities table
transform_amenities()
