import pandas as pd
import json

def extract_tabular_data(file_path: str):
    """Extract data from a tabular file_format, with pandas."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    else:
        raise Exception("invalid File extension")

def extract_json_data(file_path):
    """Extract and flatten data from a JSON file."""
    with open(file_path,"r") as f:
        data=json.load(f)
    return pd.json_normalize(data)

def extract_json_data(file_path):
    """Extract and flatten data from a JSON file."""
    with open(file_path,"r") as f:
        data=json.load(f)
    return pd.json_normalize(data)

def transform_electricity_sales_data(raw_data: pd.DataFrame):
    """
    Transform electricity sales to find the total amount of electricity sold
    in the residential and transportation sectors.
    
    To transform the electricity sales data, you'll need to do the following:
    - Drop any records with NA values in the `price` column. Do this inplace.
    - Only keep records with a `sectorName` of "residential" or "transportation".
    - Create a `month` column using the first 4 characters of the values in `period`.
    - Create a `year` column using the last 2 characters of the values in `period`.
    - Return the transformed `DataFrame`, keeping only the columns `year`, `month`, `stateid`, `price` and `price-units`.
    """
    raw_data.dropna(subset=["price"],inplace=True)
    cleaned_df=raw_data[raw_data['sectorName'].isin(["residential","transportation"])]
    cleaned_df["month"]=cleaned_df["period"].str[0:4]
    cleaned_df["year"]=cleaned_df["period"].str[-2:]
    final_columns=['year','month','stateid','price','price-units']
    return cleaned_df[final_columns]

def load(dataframe: pd.DataFrame, file_path: str):
    """Load a DataFrame to a file in either CSV or Parquet format."""
    if file_path.endswith(".csv"):
         dataframe.to_csv(file_path,index=False)
    elif file_path.endswith(".parquet"):
         dataframe.to_parquet(file_path,index=False)
    else: 
         raise Exception (f" {file_path} is invalid")
        

# Ready for the moment of truth? It's time to test the functions that you wrote!
raw_electricity_capability_df = extract_json_data("electricity_capability_nested.json")
raw_electricity_sales_df = extract_tabular_data("electricity_sales.csv")

cleaned_electricity_sales_df = transform_electricity_sales_data(raw_electricity_sales_df)

load(raw_electricity_capability_df, "loaded__electricity_capability.parquet")
load(cleaned_electricity_sales_df, "loaded__electricity_sales.csv")
