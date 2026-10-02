# 1. Imports
import pandas as pd
import numpy as np
import sqlite3

# 2. Extract
# Read CSV
def extract_data():
    data=pd.read_csv("../data/sample-sales.csv")
    return data
#=============
# Intital Inspection
#================
# print(data.head())
# print(data.shape)
# print(data.columns)

# #==============
# 3 Data Quality Checks
# #=================
def validate_data(data):
    print("Missing values:")
    print(data.isnull().sum())

    print("Duplicate rows:")
    print(data.duplicated().sum())

    print("Duplicated rows:")
    print(data['order_id'].duplicated().sum())

    print("Data Types:")
    print(data.dtypes)

    
#==================
# Validate total
#==============

    data['calculated_total']=(data['quantity']*data['unit_price']).round(2)

    incorrect_totals=(data['total']!= data['calculated_total']).sum()

    print("incorrect_total:",incorrect_totals)


    data=data.drop(columns=["calculated_total"])

    return data
#=========================

def transform_data(data):

# 4. Transform
#===========================
    # print(data['date'])
    # Convert date
    data['date']=pd.to_datetime(data['date'])
    # print(data['date'].dtype)
    # print(data['date'])

    # month
    data['month']=data['date'].dt.month
    #month name
    data['month_name']=data['date'].dt.month_name()
    # print(data[['date','month','month_name']])

    # order size
    data['size']=np.select(
        [
            data['total']<200,
            data['total']<500
        ],
        ["Low",
        "Medium"],
        default="High"
    )
    # print(data[['total','size']])

    print(data.columns)

    return data
# ====================
# Loading to database
# ==================
def load_data(data):

# Connect to SQLite

    conn=sqlite3.connect("../database/sales.db")

    # Write dataframe to sales table

    data.to_sql("sales",conn,if_exists='replace',index=False)

    print(pd.read_sql("SELECT * FROM sales LIMIT 5",conn))

    print(pd.read_sql("SELECT SUM(total) AS total_revenue FROM sales",conn))

    print(pd.read_sql('SELECT product,SUM(total) AS total_revenue FROM sales  GROUP BY product ORDER BY total_revenue DESC ',conn))

    print(pd.read_sql('SELECT region,SUM(total)AS revenue FROM sales GROUP BY region ORDER BY revenue DESC',conn))

    print(pd.read_sql('SELECT salesperson,SUM(total) AS revenue FROM sales GROUP BY salesperson ORDER BY revenue DESC',conn))

    print(pd.read_sql("SELECT month,month_name,SUM(total)AS revenue FROM sales GROUP BY month,month_name ORDER BY month",conn))

    # closing
    conn.close()

def main():
    data=extract_data()
    data=validate_data(data)
    data=transform_data(data)
    load_data(data)

if __name__ == "__main__":
    main()