# The web scraping includes Overview, The Unit The Building and Accesibility sections of the page
# example: https://www.kijiji.ca/v-apartments-condos/city-of-halifax/spacious-3-bed-condo-on-lacewood-drive-for-rent/1688431972

# import the necessary libraries
import requests
import pandas as pd 
from bs4 import BeautifulSoup

def url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return False

def get_soup(url):
    # use requests library to get respo
    response = requests.get(url)
    # use BS to parse the text of the HTML response
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_ad_links(url):
    # WEB CRAWLING
    # find all of the relevant ads
    #ads = soup.find_all("li", attrs={"data-testid": ["srp-search-list"], "class": ["sc-68931dd3-0", "dFkkEs"]})[0]
    ads = get_soup(url).find_all('li', attrs={'data-testid': True})
    ad_links = []
    for ad in ads:
        # parse the link from the ad
        link = ad.find_all('a', attrs={'data-testid': 'listing-link'})
        # add the link to the list
        for l in link:
            ad_links.append(base_url + l["href"])
    return ad_links

def get_title(soup):
    # get ad title
    try:
        title = soup.find("h1", class_='title-4206718449').text
    except AttributeError:
        title = "NA"
    # print("Title: ", title)
    return title

def get_price(soup):
    price_tag = soup.find('span', {'content': True})
    if price_tag:
        price = price_tag['content']
    else:
        price = "NA"
    # print("Price: ", price)
    return price

def get_date_posted(soup):
    try:
        date_posted = time_tag = soup.find('time')['datetime']
    except (AttributeError, TypeError):
        date_posted = "NA"
    # print(date_posted)
    return date_posted

def get_address(soup):
    try:
        address = soup.find("span", attrs={"itemprop": "address"}).text
    except AttributeError:
        address = "NA"
    # print(address)
    return address

def get_type_bed_bath(soup):
    try:
        # Initialize variables to store rental type, number of bedrooms, and number of bathrooms
        rental_type = num_bedrooms = num_bathrooms = "NA"

        # Find all <li> elements within the <div> with class 'titleAttributes-183069789'
        attribute_elements = soup.find('div', class_='titleAttributes-183069789').find_all('li', class_='noLabelAttribute-262950866')

        for element in attribute_elements:
            # Extract the text value
            text = element.find('span', class_='noLabelValue-774086477').text.strip()
            
            # Check which attribute it is and assign the value accordingly
            if 'Bedrooms' in text:
                num_bedrooms = text.split(': ')[1]
            elif 'Bathrooms' in text:
                num_bathrooms = text.split(': ')[1]
            else:
                rental_type = text
        # print("Rental Type:", rental_type)
        # print("Number of Bedrooms:", num_bedrooms)
        # print("Number of Bathrooms:", num_bathrooms)
    except:
        attribute_list = soup.find('div', class_='attributeListWrapper-1686160158')
        if attribute_list:
            bedrooms_tag = attribute_list.find('dt', text='Bedrooms')
            bathrooms_tag = attribute_list.find('dt', text='Bathrooms')
            bedrooms = bedrooms_tag.find_next_sibling('dd').text if bedrooms_tag else 'NA'
            bathrooms = bathrooms_tag.find_next_sibling('dd').text if bathrooms_tag else 'NA'
            num_bedrooms = bedrooms
            num_bathrooms = bathrooms
        #print("Type, no. of bedrooma and bath not available")

    return rental_type, num_bedrooms, num_bathrooms

def get_company(soup):
    try:
        # find the <a> tag within the <div> with class 'header-1351916284'
        company = soup.find('div', class_='header-1351916284').find('a', class_='link-441721484').get_text()
    except AttributeError:
        company = "NA"
    # print("Company: ", company)
    return company

def get_company_type(soup):
    try:
        # find the div with class 'line-794739306'
        company_type = soup.find('div', class_='line-794739306').get_text()
    except AttributeError:
        company_type = "NA"
    # print("Company Type: ", company_type)
    return company_type

def get_singleline_attrs(soup):
    singleline_attributes = {
        "Parking Included": "NA",
        "Agreement Type": "NA",
        "Pet Friendly": "NA",
        "Move-In Date": "NA",
        "Size (sqft)": "NA",
        "Furnished": "NA",
        "Air Conditioning": "NA",
        "Smoking Permitted": "NA",
        "Elevator Accessibility Features": "NA",
        "Barrier-free Entrances and Ramps": "NA",
        "Visual Aids": "NA",
        "Accessible Washrooms in Suite": "NA",
    }

    # Find all <li> elements with class 'twoLinesAttribute-633292638' which contain attribute information
    attribute_elements = soup.find_all('li', class_='twoLinesAttribute-633292638')

    for element in attribute_elements:
        # Extract the label and value
        label = element.find('dt', class_='twoLinesLabel-2332083105').text.strip()
        value = element.find('dd', class_='twoLinesValue-2653438411').text.strip()
        singleline_attributes[label] = value
    # print(singleline_attributes)
    return singleline_attributes

def get_multiline_attrs(soup):
    # Initialize
    multiline_attributes = {
        'heat': 'No',
        'hydro': 'No',
        'water': 'No',
        'cable_tv': 'No',
        'internet': 'No',
        'laundry_unit': 'No',
        'laundry_building': 'No',
        'dishwasher': 'No',
        'fridge_freezer': 'No',
        'yard': 'No',
        'balcony': 'No',
        'building_security': 'No',
        'building_elevator': 'No',
        'building_gym': 'No',
        'bycycle_parking': 'No',
        'storage_space': 'No'
    }

    # Find all <li> elements with class 'attributeGroupContainer-1655609067' which contain attribute group information
    multiline_elements = soup.find_all('li', class_='attributeGroupContainer-1655609067')

    for element in multiline_elements:
        # Extract the group title
        group_title = element.find('h4', class_='attributeGroupTitle-889029213').text.strip()
        # Extract the items within the group
        group_items = element.find_all('li', class_='groupItem-1182798569')
        # Check if the group title is 'Wi-Fi and More'
        if group_title == 'Utilities Included':
            # Iterate through group items
            for item in group_items:
                # Extract utility name and availability status
                utility_name = item.text.strip()
                utility_available = item.find('svg', class_='yesNoIcon-3463566473')

                # Check if utility is available based on aria-label attribute of svg element
                if utility_name == 'Heat':
                    multiline_attributes['heat'] = "Yes" if utility_available and "Yes" in utility_available['aria-label'] else "No"
                elif utility_name == 'Hydro':
                    multiline_attributes['hydro'] = "Yes" if utility_available and "Yes" in utility_available['aria-label'] else "No"
                elif utility_name == 'Water':
                    multiline_attributes['water'] = "Yes" if utility_available and "Yes" in utility_available['aria-label'] else "No"
        
        elif group_title == 'Wi-Fi and More':
            # Iterate through group items
            for item in group_items:
                # Extract the utility name
                utility_name = item.text.strip()
                # Check if the utility is Cable/TV or Internet
                if utility_name == 'Cable / TV':
                    multiline_attributes['cable_tv'] = "Yes"
                elif utility_name == 'Internet':
                    multiline_attributes['internet'] = "Yes"

        # Check if the group title is 'Appliances'
        elif group_title == 'Appliances':
            # Iterate through group items
            for item in group_items:
                # Extract the utility name
                utility_name = item.text.strip()

                # Check if the utility is Laundry (In Unit), Dishwasher, or Fridge / Freezer
                if utility_name == 'Laundry (In Unit)':
                    multiline_attributes['laundry_unit'] = "Yes"
                elif utility_name == 'Laundry (In Building)':
                    multiline_attributes['laundry_building'] = "Yes"
                elif utility_name == 'Dishwasher':
                    multiline_attributes['dishwasher'] = "Yes"
                elif utility_name == 'Fridge / Freezer':
                    multiline_attributes['fridge_freezer'] = "Yes"
        
        # Check if the group title is 'Personal Outdoor Space'
        elif group_title == 'Personal Outdoor Space':
            # Iterate through group items
            for item in group_items:
                # Extract the outdoor space feature
                outdoor_feature = item.text.strip()

                # Check if the outdoor feature is Yard or Balcony
                if outdoor_feature == 'Yard':
                    multiline_attributes['yard'] = "Yes"
                elif outdoor_feature == 'Balcony':
                    multiline_attributes['balcony'] = "Yes"
        
        elif group_title == 'Amenities':
            # Iterate through group items
            for item in group_items:
                # Extract the utility name
                utility_name = item.text.strip()
                # Check if the utility is Cable/TV or Internet
                if utility_name == '24 Hour Security':
                    multiline_attributes['building_security'] = "Yes"
                elif utility_name == 'Elevator in Building':
                    multiline_attributes['building_elevator'] = "Yes"
                elif utility_name == 'Gym':
                    multiline_attributes['building_gym'] = "Yes"
                elif utility_name == 'Bicycle Parking':
                    multiline_attributes['bycycle_parking'] = "Yes"
                elif utility_name == 'Storage Space':
                    multiline_attributes['storage_space'] = "Yes"
    # for key, value in multiline_attributes.items():
    #     print(f"{key.capitalize()}: {value}")

    return multiline_attributes

# Main
if __name__ == "__main__":
     # base URL for the Kijiji website
    base_url = "https://www.kijiji.ca"
    page_url = base_url + "/b-for-rent/city-of-halifax/c30349001l1700321"
    page_no = 1
    while url_exists(page_url):

        # Get page links
        ad_links = get_ad_links(page_url)

        # Scraping - Collecting Data
        ## create a list to store dictionaries of our results
        data_list = []
        ad_no = 1
        for advert in ad_links:
            print("\n######################################################")
            print("Page: ", page_no, "Ad No.", ad_no)
            print("ad link: ", advert)

            # grab webpage information & transform with BS
            soup = get_soup(advert)

            # Get ad title
            title = get_title(soup)

            # get ad price
            price = get_price(soup)

            # get date posted
            date_posted = get_date_posted(soup)

            # get the ad address
            address = get_address(soup)

            # Get ad type i.e. house, apartment etc
            rental_type, num_bedrooms, num_bathrooms = get_type_bed_bath(soup)

            #listing company
            company = get_company(soup)

            # get listed by i.e. owner/professional
            company_type = get_company_type(soup)

            # Single Line attributes
            singleline_attributes = get_singleline_attrs(soup)

            # Multiline attributes
            multiline_attributes = get_multiline_attrs(soup)

            # append information to the list of dictionaries
            data_list.append({
                "title": title,
                "price": price,
                "date_posted": date_posted,
                "address": address,
                "rental_type": rental_type,
                "num_bedrooms": num_bedrooms,
                "num_bathrooms": num_bathrooms,
                "url": advert,
                "company": company,
                "company_type": company_type,
                **singleline_attributes,
                **multiline_attributes,
            })

            # create DataFrame from the list of dictionaries
            df = pd.DataFrame(data_list)
            # save the final dataframe to a csv file
            df.to_csv("kijiji_real_estate_data.csv", mode='a', index=False)
            # Ad no increment
            ad_no += 1
        page_no += 1
        page_url = base_url + "/b-for-rent/city-of-halifax/page-" + str(page_no) + "/c30349001l1700321"
