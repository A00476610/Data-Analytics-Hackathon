from ..llm_core.models import Amenities



from django.core.management.base import BaseCommand
from your_app_name.models import Amenities


def amenities_count():
    amenities = Amenities.objects.all()

    for amenity in amenities:
        # Calculate the sum of True values for boolean fields
        true_count = sum([
            amenity.furnished, amenity.air_conditioning, amenity.heat, amenity.hydro,
            amenity.water, amenity.cable_tv, amenity.internet, amenity.laundry_unit,
            amenity.laundry_building, amenity.dishwasher, amenity.fridge_freezer,
            amenity.yard, amenity.balcony, amenity.building_security, amenity.building_elevator,
            amenity.building_gym, amenity.bycycle_parking, amenity.storage_space
        ])
        # Update amenities_count and save
        amenity.amenities_count = true_count
        amenity.save()

amenities_count()
