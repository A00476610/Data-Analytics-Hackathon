# src/extract.py
import pandas as pd

def extract(file_path, new_headers):
  """
  Extracts data from a CSV file, renaming the header names.

  Args:
      file_path (str): The path to the CSV file.
      new_headers (list): A list of desired new header names.

  Returns:
      pandas.DataFrame: The extracted data as a DataFrame with renamed headers.
  """

  try:
    data = pd.read_csv(file_path, header=0)
     # If new headers provided, rename them
    if new_headers is not None:
      data = data.rename(columns=dict(zip(data.columns, new_headers)))

    return data
  except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    return None
  except pd.errors.ParserError:
    print(f"Error: Could not parse CSV file at {file_path}")
    return None