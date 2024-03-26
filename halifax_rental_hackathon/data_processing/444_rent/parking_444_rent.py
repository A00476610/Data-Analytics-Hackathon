import pandas as pd

class Parking_444_Rent:

    def __init__(self, raw_csv, clean_csv):
        self.raw_csv = raw_csv
        self.clean_csv = clean_csv

    def extract(self):
        df = pd.read_csv(self.raw_csv)
        return df

    def transform(self, df):
        # Remove duplicate rows
        df.drop_duplicates(inplace=True)
        
        # Delete the extra columns
        df.drop('parking', axis=1, inplace=True)
        df.drop('rate', axis=1, inplace=True)
        
        # Strip the commas from column
        df['available'] = df['available'].str.replace(',', '')
        df['term'] = df['term'].str.replace(',', '')
        
        # Clean the column - remove the dollar sign ($) and any commas
        df['price'] = df['price'].str.replace('$', '')
        df['deposit'] = df['deposit'].str.replace('$', '')
        df['deposit'] = df['deposit'].str.replace(',', '')
        # Convert the column to float
        df['price'] = df['price'].astype(float)
        df['deposit'] = df['deposit'].astype(float)

        # Fill Na
        df.fillna({'TENANT SERVICES COORDINATOR': 'Not Available'}, inplace=True)
        df.fillna({'RESIDENT MANAGERS': 'Not Available'}, inplace=True)
        df.fillna({'COMMERCIAL PROPERTY MANAGER': 'Not Available'}, inplace=True)
        df.fillna({'email': 'Not Available'}, inplace=True)
        df.fillna({'Website': 'http://www.444rent.com'}, inplace=True)
        df.fillna({'fax': 'Not Available'}, inplace=True)
        df.fillna({'termination policy': 'Not Available'}, inplace=True)
        df.fillna({'deposit': 'Not Available'}, inplace=True)

        # Lowercase all headers
        df.columns = df.columns.str.lower()  
        return df
    
    def load(self, df):
        # Save the cleaned CSV file
        df.to_csv(self.clean_csv, index=False)

if __name__ == '__main__':
    RAW_CSV = "D:/hackathon/Data-Analytics-Hackathon/halifax_rental_hackathon/scrapers/444_rent/parking_444_rent.csv"
    CLEAN_CSV = '../clean_data/clean_parking_444_rent.csv'

    parking_444_rent = Parking_444_Rent(RAW_CSV, CLEAN_CSV)
    # Extract data
    df = parking_444_rent.extract()

    # Transform Data
    df = parking_444_rent.transform(df)
    
    # Load CSV data
    df = parking_444_rent.load(df)
