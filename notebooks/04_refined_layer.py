# Databricks notebook source
# MAGIC %md
# MAGIC # Capa Refined: KPIs y Gobierno
# MAGIC Generación de métricas de negocio y reporte de calidad de datos.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from datetime import datetime

# Configuración
user_name = "OscarGuio"
catalog = f"nyc_taxi_{user_name}"
trusted_schema = f"{catalog}.trusted"
refined_schema = f"{catalog}.refined"

# COMMAND ----------

# Lectura de Trusted
df = spark.read.table(f"{trusted_schema}.trips_cleaned")

# COMMAND ----------

# KPI 1: Patrón de demanda temporal
# Definir franjas horarias
# 0-4: Trasnochón, 4-8: Madrugada, 8-12: Mañana, 12-16: Mediodía, 16-20: Tarde, 20-24: Noche
df_temporal = df.withColumn("hour", F.hour("tpep_pickup_datetime")) \
                .withColumn("day_of_week", F.date_format("tpep_pickup_datetime", "EEEE")) \
                .withColumn("duration_min", (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60) \
                .withColumn("time_slot", 
                    F.when((F.col("hour") >= 0) & (F.col("hour") < 4), "Trasnochón")
                    .when((F.col("hour") >= 4) & (F.col("hour") < 8), "Madrugada")
                    .when((F.col("hour") >= 8) & (F.col("hour") < 12), "Mañana")
                    .when((F.col("hour") >= 12) & (F.col("hour") < 16), "Mediodía")
                    .when((F.col("hour") >= 16) & (F.col("hour") < 20), "Tarde")
                    .otherwise("Noche"))

kpi_temporal = df_temporal.groupBy("day_of_week", "time_slot").agg(
    F.count("*").alias("total_trips"),
    F.avg("duration_min").alias("avg_duration_min"),
    F.avg("fare_amount").alias("avg_fare_amount")
).orderBy("day_of_week", "time_slot")

kpi_temporal.write.format("delta").mode("overwrite").saveAsTable(f"{refined_schema}.kpi_demand_patterns")

# COMMAND ----------

# KPI 2: Eficiencia económica por zona
df_efficiency = df_temporal.withColumn("speed_mph", F.col("trip_distance") / (F.col("duration_min") / 60)) \
                           .withColumn("income_per_mile", F.col("fare_amount") / F.col("trip_distance"))

kpi_efficiency = df_efficiency.groupBy("pickup_borough", "pickup_zone").agg(
    F.avg("income_per_mile").alias("avg_income_per_mile"),
    F.avg("speed_mph").alias("avg_speed_mph"),
    F.count("*").alias("trip_count")
)

# Top 10 zonas más rentables
kpi_top_zones = kpi_efficiency.orderBy(F.desc("avg_income_per_mile")).limit(10)

kpi_efficiency.write.format("delta").mode("overwrite").saveAsTable(f"{refined_schema}.kpi_zone_efficiency")

# COMMAND ----------

# GOBIERNO: Data Quality Report (Expectations)
# Re-calculamos sobre raw para ver el impacto
df_raw = spark.read.table(f"{catalog}.raw.yellow_taxi_trips")

dq_report = df_raw.select(
    F.lit(datetime.now()).alias("execution_date"),
    F.count("*").alias("total_records"),
    F.sum(F.when(F.col("tpep_pickup_datetime") >= F.col("tpep_dropoff_datetime"), 1).otherwise(0)).alias("fail_dates"),
    F.sum(F.when(F.col("trip_distance") <= 0, 1).otherwise(0)).alias("fail_distance"),
    F.sum(F.when(F.col("fare_amount") <= 0, 1).otherwise(0)).alias("fail_fare")
)

dq_report.write.format("delta").mode("overwrite").saveAsTable(f"{refined_schema}.data_quality_report")

print("Capa Refined completada. KPIs y Reporte de Calidad generados.")
