# Databricks notebook source
# MAGIC %md
# MAGIC # Setup: Unity Catalog Structure
# MAGIC Define el catálogo y los esquemas para la arquitectura Medallion.

# COMMAND ----------

# Configuración de nombres 
user_name = "OscarGuio" # Cambiar por tu nombre
catalog_name = f"nyc_taxi_{user_name}"

# COMMAND ----------

# Crear Catálogo si no existe
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
print(f"Catálogo {catalog_name} verificado/creado.")

# COMMAND ----------

# Crear Esquemas (Schemas)
schemas = ["raw", "trusted", "refined"]

for schema in schemas:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema}")
    print(f"Esquema {schema} verificado/creado en {catalog_name}.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Referencias de Origen
# MAGIC - **Dataset Parquet (Enero 2023):** `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet`
# MAGIC - **Taxi Zone Lookup (CSV):** `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`
