import pandas as pd
trips = pd.read_parquet("/Users/pranavkumarkaparthi/Desktop/Practice Datasets/nyc_taxi_pipeline/data/raw/yellow_tripdata_2022-01.parquet")
print(trips.shape)

from pyiceberg.catalog import load_catalog

config = {
    "type": "sql",
    "uri": "sqlite:///catalog.db",
    "warehouse": "warehouse",
}
catalog = load_catalog("lab", **config)
#####catalog.create_namespace("nyc")

if("nyc",) not in catalog.list_namespaces():
    catalog.create_namespace("nyc")
print(catalog.list_namespaces())


