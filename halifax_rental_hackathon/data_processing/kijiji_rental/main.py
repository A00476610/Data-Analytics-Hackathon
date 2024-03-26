# main.py
import pandas as pd
from src.extract import extract
from src.transform import transform
from src.load import load_to_csv
from src.logger import log_progress

def main():
    # table_name = "kijiji" - db table name
    table_attributes = ['title', 'price', 'date_posted', 'address', 'rental_type', 'num_bedrooms', 'num_bathrooms', 'url', 'company', 'company_type', 'num_parking', 'agreement_type',	'pet_friendly',	'move_in_date', 'size_sqft', 'furnished', 'air_conditioning', 'smoking_permitted', 'elevator_accessibility_features', 'barrier_free_entrances_ramps', 'visual_aids', 'accessible_washrooms_in_suite', 'heat', 'hydro', 'water', 'cable_tv', 'internet', 'laundry_unit', 'laundry_building', 'dishwasher', 'fridge_freezer', 'yard', 'balcony', 'building_security', 'building_elevator', 'building_gym', 'bycycle_parking', 'storage_space']
    # db_path = "data/World_Economies.db"
    RAW_CSV_PATH = "../raw_data/kijiji_real_estate_data.csv"
    CLEAN_CSV_PATH = "../clean_data/clean_kijiji_real_estate_data.csv"
    # query_statement = "SELECT"
    log_progress("Preliminaries complete. Initiating ETL process.")

    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 
    df = extract(RAW_CSV_PATH, table_attributes)
    
    # Log the completion of the Extraction process 
    log_progress("Extract phase Ended") 

    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 
    transformed_data = transform(df)
    #print(transformed_data['num_bedrooms'].head(10))
    # print("Transformed Data") 
    # print(transformed_data) 

    # Log the completion of the Transformation process 
    log_progress("Transform phase Ended") 
    
    # Log the beginning of the Loading process 
    log_progress("Load to csv phase Started") 
    load_to_csv(transformed_data, CLEAN_CSV_PATH)

    # # Log the completion of the Loading process 
    # log_progress("Load to csv phase Ended", log_file) 

    # # Log the beginning of the Loading process 
    # log_progress("Load to db phase Started", log_file) 
    # conn = sqlite3.connect(db_path)
    # load_to_db(transformed_data, conn, table_name)

    # # Log the completion of the Loading process 
    # log_progress("Load to db phase Ended", log_file) 
    
    # # Log the completion of the ETL process 
    # log_progress("ETL Job Ended", log_file) 

    # # Log the beginning of the Querying process 
    # log_progress("Querying phase Started", log_file) 
    # query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
    # run_query(query_statement, db_path)

    # # Log the completion of the Querying process
    # log_progress("Query process completed", log_file) 

if __name__ == "__main__":
    main()