from pyiceberg.catalog import load_catalog

config = {
    "type": "sql",
    "uri": "sqlite:///catalog_s3.db",
    "warehouse": "s3://warehouse/",
    "s3.endpoint": "http://localhost:9000",
    "s3.access-key-id": "admin",
    "s3.secret-access-key": "password",
    "s3.region": "us-east-1",
    "s3.path-style-access": "true",
}

catalog_s3 = load_catalog("lab_s3", **config)

if ("nyc",) not in catalog_s3.list_namespaces():
    catalog_s3.create_namespace("nyc")

print(catalog_s3.list_namespaces())
