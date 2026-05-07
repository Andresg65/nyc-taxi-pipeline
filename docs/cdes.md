# Critical Data Elements (CDEs) - NYC Taxi

Identificación y documentación de los elementos críticos para el negocio y la calidad del proceso.

| CDE | Definición de Negocio | Regla de Calidad | Tabla / Columna |
| :--- | :--- | :--- | :--- |
| **Fecha de Recogida** | Marca de tiempo exacta en que el pasajero aborda el taxi. | Debe ser menor a la fecha de entrega y no ser nula. | `trusted.trips` / `tpep_pickup_datetime` |
| **Distancia del Viaje** | Kilometraje total recorrido durante el servicio en millas. | Debe ser un valor numérico estrictamente mayor a 0. | `trusted.trips` / `trip_distance` |
| **Monto de la Tarifa** | Valor base cobrado al pasajero (excluyendo propinas y peajes). | Debe ser un valor numérico mayor a 0. | `trusted.trips` / `fare_amount` |
