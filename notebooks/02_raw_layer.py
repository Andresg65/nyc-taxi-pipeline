# Databricks notebook source
# MAGIC %md
# MAGIC # Capa Raw: Ingesta de Datos
# MAGIC Carga los datos de origen (Parquet y CSV) a tablas Delta sin transformaciones complejas.

# COMMAND ----------

import requests
import os

# Configuración
user_name = "OscarGuio"
catalog = f"nyc_taxi_{user_name}"
raw_schema = f"{catalog}.raw"

# URLs de origen
trips_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
zones_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

# Directorio en Unity Catalog Volume
# Formato: /Volumes/<catalog>/<schema>/<volume>/
temp_dir = f"/Volumes/{catalog}/raw/ingestion_volume/"

# COMMAND ----------

def download_file(url, target_path):
    print(f"Descargando {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            f.write(response.content)
        print(f"Descargado exitosamente en {target_path}")
    else:
        raise Exception(f"Error al descargar: {response.status_code}")

# COMMAND ----------

# Descargar archivos a la zona local del driver y luego mover a DBFS
local_trips = "/tmp/trips_2023_01.parquet"
local_zones = "/tmp/taxi_zones.csv"

download_file(trips_url, local_trips)
download_file(zones_url, local_zones)

dbutils.fs.cp(f"file:{local_trips}", f"{temp_dir}trips.parquet")
dbutils.fs.cp(f"file:{local_zones}", f"{temp_dir}zones.csv")

# COMMAND ----------

# Ingesta a Capa Raw (Trips)
print("Ingestando Trips a Raw...")
df_trips = spark.read.parquet(f"{temp_dir}trips.parquet")
df_trips.write.format("delta").mode("overwrite").saveAsTable(f"{raw_schema}.yellow_taxi_trips")

# Ingesta a Capa Raw (Zones)
print("Ingestando Zones a Raw...")
df_zones = spark.read.option("header", "true").csv(f"{temp_dir}zones.csv")
df_zones.write.format("delta").mode("overwrite").saveAsTable(f"{raw_schema}.taxi_zone_lookup")

print(f"Capa Raw completada. Tablas creadas en {raw_schema}")
