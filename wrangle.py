import pandas as pd
import os
from env import user, password, host

def get_db_url(database):
    return f'mysql+pymysql://{user}:{password}@{host}/{database}'


def get_zillow_data():

    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_new_zillow_data()

def get_new_zillow_data():

    sql = """
    select 
    bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    join propertylandusetype using (propertylandusetypeid)
    where propertylandusedesc = "Single Family Residential"
    """
    return pd.read_sql(sql, get_db_url("zillow"))

def rename_cols(df): #rename columns
    df = df.rename(columns = {'bedroomcnt':'bedroom_cnt', 'bathroomcnt':'bath_cnt', 'calculatedfinishedsquarefeet':'SqFt', 'taxvaluedollarcnt':'tax_value', 'yearbuilt':'year_built', 'taxamount':'tax_amount'})
    return df

def handle_nulls(df):    
    df = df.dropna()
    return df


def optimize_types(df):
    # Convert some columns to integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)    
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    return df


def handle_outliers(df):
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 2_000_000]

    return df


def wrangle_zillow():
 
    df = get_zillow_data()

    df = handle_nulls(df)

    df = optimize_types(df)

    df = handle_outliers(df)

    df = rename_cols(df)

    df.to_csv("zillow.csv", index=False)

    return df
