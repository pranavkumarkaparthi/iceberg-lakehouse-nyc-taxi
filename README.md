# NYC Taxi Lakehouse — Apache Iceberg with PyIceberg

A hands-on Apache Iceberg lakehouse built with PyIceberg on **2,463,931 NYC yellow taxi trips (January 2022)**. The project walks the full life of an Iceberg table: profiling the raw data, loading it in two snapshots, reading the table's own metadata, time travel, schema evolution, hidden partitioning with partition pruning, a cross-engine read with DuckDB, and finally moving the table's warehouse from local disk to S3-compatible object storage (MinIO).

## Dataset

- `yellow_tripdata_2022-01.parquet` — 2,463,931 rows × 19 columns
- Profiled **before** loading (shape, dtypes, nulls, uniqueness, value sanity): 71,503 nulls across exactly 5 columns; zero duplicate rows; no primary key (an event log); 52 rows fall outside January 2022. Data was loaded **as-is** — the profiling results serve as the answer key for every later verification.

## Architecture

- **Catalog:** SQLite (Iceberg SQL catalog) — two instances, one per warehouse
- **Table format:** Apache Iceberg, format version 2
- **Storage:** local filesystem, then MinIO (S3-compatible object storage)
- **Engines:** PyIceberg (build / write / read) and DuckDB (independent verification reads)

## What was built — and verified

1. **`nyc.taxi_trips`** — unpartitioned table loaded in two appends: Snapshot 1 = 1,000,000 rows; Snapshot 2 = 2,463,931 total, parent-linked to Snapshot 1.
2. **Metadata inspection** — read the real `metadata.json`: snapshot graph, schema field IDs 1–19, empty partition spec.
3. **Time travel** — a scan pinned to Snapshot 1 returns exactly 1,000,000 rows while the current table reads 2,463,931.
4. **Schema evolution** — added `ingest_batch` (field ID 20, optional string) as a metadata-only change: a new `metadata.json`, snapshots unchanged at 2, **zero data files rewritten**.
5. **Hidden partitioning** — `nyc.taxi_trips_day`, partitioned by `day(tpep_pickup_datetime)` (partition field `1000: pickup_day`). One append wrote **40 data files** (31 January days + 9 stray days). A scan filtered to 2022-01-15 planned **1 of 40 files** (partition pruning) and returned **88,704 rows** — matching an independent pandas answer key exactly.
6. **Engine independence** — DuckDB (`iceberg` extension, `iceberg_scan`) read the PyIceberg-written table and reproduced both counts: **2,463,931** total; **88,704** for 2022-01-15.
7. **Object storage** — the partitioned table was recreated in MinIO at `s3://warehouse/nyc/taxi_trips_day` with schema and partition spec copied from the disk table; the append wrote **44 objects** (40 data + 4 metadata) and scans read 2,463,931 back from S3 storage.

## Repo layout

- `profile.py` — the pre-load profiling battery on the raw Parquet (shape, dtypes, nulls, duplicates, uniqueness, ranges, out-of-month rows)
- `lakehouse.py` — catalog config + raw-data load for the local-disk warehouse
- `lakehouse_s3.py` — catalog config for the MinIO (S3) warehouse
- `warehouse/` and the catalog databases are generated artifacts (git-ignored); the raw dataset is not included — the tables are fully regenerable from the two recipe files.

## Notes

- The MinIO credentials in `lakehouse_s3.py` are the local course stack's public defaults, for a laptop-only dev environment. Production systems inject credentials via environment variables or a secrets manager — never code.
- Snapshot expiration is not exposed by this PyIceberg build's maintenance API; in production it is run via Spark (`CALL system.expire_snapshots`) or Athena (`VACUUM`).

## Stack

Python 3.11 · PyIceberg (+ pyiceberg-core) · PyArrow · pandas · DuckDB · MinIO · SQLite catalog
