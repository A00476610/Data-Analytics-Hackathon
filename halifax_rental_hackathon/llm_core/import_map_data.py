import csv
import os
import re

from llm_core.models import Construction 

# Define the CSV file path directly
csv_file_path = 'D:/hackathon/Data-Analytics-Hackathon/halifax_rental_hackathon/data_processing/raw_data/map_data.csv'  # Replace with your actual path

def clean_floors(floor_str):
    match = re.search(r'\d+', floor_str)  # Extract the first number
    return int(match.group()) if match else 0

with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile) 
    next(reader)  # Skip the header row 

    for row in reader:
        
        project = Construction(
            property_name=row[0],
            civic_address=row[1],
            floors=clean_floors(row[2]),
            units=int(row[3]) if (row[3] != 'TBD' and row[3] != '') else 0,
            developer=row[4],
            status=row[5],
            website=row[6],
            property_type=row[7],
            completion_estimate=row[8],
            retail_sq_ft=int(row[9].replace(',', '')) if (row[9] != 'TBD' and row[9] != '' and row[9]) else None,
            district=row[10],
            image_url=row[11]
        )
        project.save()
