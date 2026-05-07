# Glosario de Negocio - NYC Taxi Pipeline

Este documento define los términos clave utilizados en el dominio de datos de viajes de taxis amarillos en NYC.

| Término | Definición |
| :--- | :--- |
| **Viaje Válido** | Un registro de viaje que cumple con las reglas mínimas de integridad: tiempo de finalización posterior al inicio, distancia recorrida mayor a cero y tarifa cobrada positiva. |
| **Borough** | División administrativa de la ciudad de Nueva York (Manhattan, Brooklyn, Queens, Bronx, Staten Island). |
| **Franja Horaria** | Segmentación del día en 6 bloques de 4 horas cada uno para analizar patrones de demanda (Madrugada, Mañana, Mediodía, Tarde, Noche, Trasnochón). |
| **Eficiencia Económica** | Ratio que mide el ingreso generado por cada milla recorrida, utilizado para identificar las zonas más rentables para los conductores. |
| **PULocationID** | Identificador numérico de la zona de inicio del viaje (Pick Up Location), vinculado a la tabla de referencia de zonas. |
