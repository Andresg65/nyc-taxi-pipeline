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

# Descargar archivos directamente al Volumen
trips_path = f"{temp_dir}trips.parquet"
zones_path = f"{temp_dir}zones.csv"

# Asegurar que el directorio del volumen sea accesible (crear subcarpeta si es necesario)
# En los Volúmenes de UC, esto se trata como un sistema de archivos local
download_file(trips_url, trips_path)
download_file(zones_url, zones_path)

# COMMAND ----------

# Ingesta a Capa Raw (Trips)
print("Ingestando Trips a Raw...")
# Leemos directamente desde la ruta del Volumen
df_trips = spark.read.parquet(trips_path)
df_trips.write.format("delta").mode("overwrite").saveAsTable(f"{raw_schema}.yellow_taxi_trips")

# Ingesta a Capa Raw (Zones)
print("Ingestando Zones a Raw...")
df_zones = spark.read.option("header", "true").csv(zones_path)
df_zones.write.format("delta").mode("overwrite").saveAsTable(f"{raw_schema}.taxi_zone_lookup")

print(f"Capa Raw completada. Tablas creadas en {raw_schema}")
