import requests

url = "https://killamreit.com/property_html"

# Setting up the payload with the provided data
payload = {
    'nids[]': ['12298', '12299', '12301', '12307', '12310', '12311', '12313', '12314', '12315', '12317', '12318', '12320', '12321', '12334', '12338', '12342', '12346', '12348', '12352', '12355', '12358', '12359', '12361', '12364', '12366', '12367', '12373', '12381', '12382', '12388', '12397', '12399', '12410', '12413', '12417', '12425', '12438', '12439', '12443', '12446', '12459', '12462', '12463', '12466', '12467', '12476', '12488', '41605', '41908', '44187', '116385', '120087', '120854', '120855', '120862', '15202310', '18951034', '42693793', '45740858', '45740969', '45745215', '45745381'],
    'sort': 'field_unit_price',
    'availability': 'now',
    'price_min': '0',
    'price_max': '0',
    'bedrooms': '-1',
    'show_map': '1',
    'location': 'Halifax, NS',
    'region': 'Halifax'
}

# Including the request headers you provided
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '',
    'Host': 'killamreit.com',
    'Origin': 'https://killamreit.com',
    'Pragma': 'no-cache',
    'Referer': 'https://killamreit.com/apartments?region=Halifax',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# Making the POST request
response = requests.post(url, data=payload, headers=headers)


# Displaying the response text (HTML, JSON, etc.)
print(response.text)
