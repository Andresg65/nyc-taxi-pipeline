# Databricks notebook source
# MAGIC %md
# MAGIC # Capa Trusted: Limpieza y Enriquecimiento
# MAGIC Aplica reglas de calidad, estandariza columnas y hace el join con zonas.

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import datetime
import json

# Configuración
user_name = "OscarGuio"
catalog = f"nyc_taxi_{user_name}"
raw_schema = f"{catalog}.raw"
trusted_schema = f"{catalog}.trusted"

# Logging setup simplificado
def log_info(msg):
    print(f"INFO: {datetime.now().isoformat()} - {msg}")

# COMMAND ----------

# Lectura de Raw
log_info("Iniciando procesamiento Capa Trusted")
df_raw = spark.read.table(f"{raw_schema}.yellow_taxi_trips")
df_zones = spark.read.table(f"{raw_schema}.taxi_zone_lookup")

total_raw = df_raw.count()
log_info(f"Registros leídos de Raw: {total_raw}")

# COMMAND ----------

# 1. Estandarización de Nombres (Convertir a snake_case si fuera necesario, aquí ya están decentes)
# Solo renombramos zonas para evitar colisiones
df_zones = df_zones.withColumnRenamed("Borough", "pickup_borough") \
                   .withColumnRenamed("Zone", "pickup_zone") \
                   .withColumnRenamed("service_zone", "pickup_service_zone")

# 2. Definición de Reglas de Calidad (Expectations)
# Regla A: pickup < dropoff
# Regla B: distance > 0 y fare > 0
df_cleaned = df_raw.withColumn("is_valid_dates", F.col("tpep_pickup_datetime") < F.col("tpep_dropoff_datetime")) \
                   .withColumn("is_valid_distance", F.col("trip_distance") > 0) \
                   .withColumn("is_valid_fare", F.col("fare_amount") > 0)

# Filtrado de nulos críticos
df_cleaned = df_cleaned.filter(F.col("tpep_pickup_datetime").isNotNull() & F.col("PULocationID").isNotNull())

# 3. Aplicar Filtros y Separar Basura (para el reporte de calidad opcional)
df_trusted = df_cleaned.filter("is_valid_dates AND is_valid_distance AND is_valid_fare")

total_trusted = df_trusted.count()
descartados = total_raw - total_trusted
log_info(f"Registros procesados exitosamente: {total_trusted}")
log_info(f"Registros descartados por calidad: {descartados}")

# 4. Join con Taxi Zones
df_enriched = df_trusted.join(df_zones, df_trusted.PULocationID == df_zones.LocationID, "left")

# 5. Guardar en Trusted
df_enriched.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{trusted_schema}.trips_cleaned")

log_info("Capa Trusted finalizada y guardada.")

# COMMAND ----------

# Reporte de Ejecución (Estructura base para el entregable final)
execution_report = {
    "stage": "Trusted",
    "timestamp": datetime.now().isoformat(),
    "total_processed": total_raw,
    "total_accepted": total_trusted,
    "total_rejected": descartados
}
print(json.dumps(execution_report, indent=2))
