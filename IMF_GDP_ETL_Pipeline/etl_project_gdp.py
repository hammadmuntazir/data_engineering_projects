# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

url='https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

json_name='Countries_by_GDP.json'
csv_name='Countries_by_GDP.csv'
table_name='Countries_by_GDP'
db_name='World_Economies.db'
log_file='etl_project_log.txt'
# attribute_list_extract =['Country', 'GDP_USD_Billion']
transformed_file="countries_by_GDP.csv"

def extract(url):
      #empty dataframe 
    df = pd.DataFrame(columns=['Country', 'GDP_USD_Million'])

    html_body=requests.get(url).text
    data=BeautifulSoup(html_body,'html.parser')
    tables=data.find_all('tbody')
    rows=tables[2].find_all('tr')
    for row in rows[3:]:
        # print(f'{row}    ,\n\n\n\n row got ended')
        columns=row.find_all('td')
        country_cells=columns[0]
        country_link=country_cells.find('a')
        country=country_link.text
        gdp=columns[2].text
        # print(gdp)
        # dictionary={'Country':country,'GDP_Billion_USD':gdp}
        if gdp and gdp != '—' and gdp.lower() not in ['n/a', 'na', '']:
            gdp_value=float(gdp.replace(',',''))
            df1 = pd.DataFrame({'Country': [country], 'GDP_USD_Million': [gdp_value]})
            df=pd.concat([df,df1],ignore_index=True)
    return df
    # print(df.to_string())
# extract()

def transform(df):
    transformed_data=pd.DataFrame()
    transformed_data['Country']=df['Country']
    # converting millions into billions
    transformed_data['GDP_USD_Billion']=(df['GDP_USD_Million']/1000).round(2)

    return transformed_data



    #  Loading DaTa to csv
def load_to_csv(target_file,transformeddata):
    transformeddata.to_csv(target_file,index=False)

    # Loading Data To Json
def load_to_json(target_file,transformeddata):
    transformeddata.to_json(target_file,orient='records', indent=2)
   #Load to database
def load_to_database(transformeddata,database_name,table_name):
    conn=sqlite3.connect(database_name)
    transformeddata.to_sql(table_name,conn,if_exists='replace',index=False)
    conn.close()

    # Querying database
def query_database(database_name,table_name):
    conn=sqlite3.connect(database_name)
    query=f"SELECT Country,GDP_USD_Billion from {table_name} WHERE GDP_USD_Billion>100 ORDER BY GDP_USD_Billion DESC LIMIT 100"
    df_result=pd.read_sql_query(query,conn)
    conn.close()
    
    df_result.to_csv('countries_above_100b.csv',index=False)

# logging
def log(message):
    timestamp=datetime.now().strftime('%Y:%B:%d %H:%M:%S')
    with open(log_file,"a")as f:
        f.write(f"{timestamp} - {message} \n")
# 
if __name__ == "__main__":
    log("=== ETL Process Started ===") 
    log("Data Extraction started ")
    extracted_data=extract(url)
    # print(extracted_data)
    log("Data Transformation started ")
    final_data=transform(extracted_data)
    log("Transformed data is loaded in csv")
    load_to_csv(csv_name,final_data)
    log("Transfomed data is loaded in Json")
    load_to_json(json_name,final_data)
    log("Transformed data is load into database")
    load_to_database(final_data,db_name,table_name)
    log('Quering countries having gdp above 100 Billion')
    query_database(db_name,table_name)
