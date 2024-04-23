import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import brotli
import csv

# The URL from which to fetch the content
url = "https://rentola.ca/for-rent/halifax-county"

# Perform the GET request
response = requests.get(url)

# Ensure the request was successful
response.raise_for_status()

# Initialize html_content
html_content = None

# Check if the content is compressed with Brotli and decompress if necessary
if 'br' in response.headers.get('Content-Encoding', ''):
    try:
        # Attempt to decompress Brotli encoded response
        html_content = brotli.decompress(response.content).decode('utf-8')
    except brotli.error:
        print("Brotli decompression failed. Using raw content instead.")
        html_content = response.content.decode('utf-8')
else:
    # If not Brotli compressed, decode the content normally
    html_content = response.content.decode('utf-8')

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <a> tags with href values containing "/listings/"
listing_urls = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].startswith('/listings/')]
listing_urls = list(set(listing_urls))

# Initialize a list to hold the responses
responses = []
all_property_details = []

# Request each URL and store the response
for listing_url in listing_urls:
    print(f"Requesting: {listing_url}")
    listing_response = requests.get(listing_url)

    # Check if the response is Brotli encoded
    content = None
    if 'br' in listing_response.headers.get('Content-Encoding', ''):
        try:
            # Attempt to decompress Brotli encoded content
            content = brotli.decompress(listing_response.content).decode('utf-8')
        except brotli.error:
            print("Brotli decompression failed. Using raw content instead.")
            content = listing_response.content.decode('utf-8')
    else:
        # If not Brotli compressed, decode the content normally
        content = listing_response.content.decode('utf-8')

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    property_details = {}
    for circle in soup.select('.circle'):
        label = circle.select_one('.about-label').text.strip().replace(':', '')
        data = circle.select_one('.data').text.strip()
        property_details[label] = data
    
    # Extract title and location
    title_element = soup.select_one('.title')
    location_element = soup.select_one('.location')
    property_details['Title'] = title_element.text.strip() if title_element else 'N/A'
    property_details['Location'] = location_element.text.strip() if location_element else 'N/A'
    all_property_details.append(property_details)

# Determine unique fieldnames
fieldnames = set()
for details in all_property_details:
    fieldnames.update(details.keys())

# Define CSV file name
file_name = 'rentola_property_details.csv'

# Write the details to a CSV file
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for property_details in all_property_details:
        writer.writerow(property_details)

print(f"Property details have been written to {file_name}.")