import pandas as pd
trips= pd.read_parquet("/Users/pranavkumarkaparthi/Desktop/Practice Datasets/nyc_taxi_pipeline/data/raw/yellow_tripdata_2022-01.parquet")
print(trips.shape)
print(trips.head())
print(trips.dtypes)
print(trips.isnull().sum())
print(trips.duplicated().sum())
print(trips["tpep_pickup_datetime"].nunique())

print(trips["tpep_pickup_datetime"].min())
print(trips["tpep_pickup_datetime"].max())
print(trips["total_amount"].min())
print(trips["trip_distance"].max())

print(((trips["tpep_pickup_datetime"] < "2022-01-01") | (trips["tpep_pickup_datetime"] >= "2022-02-01")).sum())
