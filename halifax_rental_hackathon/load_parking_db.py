import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halifax_rental_hackathon.settings")
import django
django.setup()

import csv
from llm_core.models import Apartment, Amenities, Location, Parking  # Replace 'your_app' with your Django app name

CSV_PATH = 'D:/hackathon/Data-Analytics-Hackathon/halifax_rental_hackathon/data_processing/444_rent/clean_parking_444_rent.csv'
CSV_PATH = os.path.dirname(__file__) + '/data_processing/clean_data/clean_parking_444_rent.csv'

with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = Location(
            address=row.get('address', ''),  # Fill missing 'title' with empty string
        )
        location.save()

        parking = Parking(
            location=location,
            type=row['type'],  # Fill missing 'title' with empty string
            available=row['available'],
            price=float(row.get('price', 0.0)),  # Fill missing 'price' with 0.0
            tenant_services_coordinator=row['tenant services coordinator'],  # Fill missing 'date_posted'
            resident_managers=row['resident managers'],  # Fill missing 'move_in
            commercial_property_manager=row['commercial property manager'],
            email=row['email'],  # Fill missing 'move_in
            website=row['website'],
            tel=row['tel'],
            fax=row['fax'],
            term=row['term'],
            termination_policy=row['termination policy'],
            deposit=row['deposit'],
        )
        parking.save()

