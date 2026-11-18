# Coruña Corre

## Calidad y limpieza de los resultados

Se cargaron 5.390 filas de seis carreras. El perfil por carrera no detectó
nombres o dorsales vacíos, filas duplicadas ni dorsales repetidos dentro de
una misma prueba. Se conservaron las 5.390 filas.

| Problema | Dimensión | Carreras | Filas | Detección | Decisión |
|---|---|---|---:|---|---|
| Puesto por sexo ausente y categoría `NO` | Completitud y validez | 01 (3), 02 (6), 03 (5), 05 (3) | 17 | `—` en puesto por sexo y patrón `NO-n` en puesto por categoría | Conservar el código `NO` y su puesto de categoría. Dejar vacíos el sexo y su puesto. |
| Tiempos extremos | Validez | 05 | 3 | Tiempo convertido igual o superior a 7.200 segundos | Conservar el tiempo y marcarlo como `revisar`. El umbral se usa para detectar casos que requieren comprobación. |

## Integración y pseudonimización

El cruce con el listado de inscritos encontró 3.833 participaciones con
coincidencia de nombre normalizado y dorsal, y 1.458 sin coincidencia.
Se separaron 99 participaciones dudosas: 72 con un candidato por nombre y
dorsal distinto, y 27 con nombre ambiguo. Además, 315 dorsales aparecieron
asociados a más de un nombre entre carreras.

Los nombres se normalizaron pasando a mayúsculas, quitando tildes y
unificando espacios. Los homónimos pueden provocar uniones incorrectas y las
variantes de un nombre pueden dejar separadas participaciones de una misma
persona. Los casos dudosos se mantienen separados y se auditan en local.

Los identificadores usan HMAC-SHA256 con la clave común `CORUNA_HMAC_KEY`
guardada en `.env`. Se comprobó que la exportación conserva las 5.390 filas
y que la combinación de persona y carrera es única.

Persona 1 confirmó que `inscritos_circuito_interim.csv` contiene las 2.345
inscripciones formalizadas del circuito. El listado recoge la fecha de pago
y el dorsal asignado. La columna `estado_inscripcion` viene vacía.
Con el criterio de enlace aplicado, se clasificaron 3.833 participaciones
como `inscrito_circuito`, 1.458 como `por_prueba` y 99 como `no_resuelto`.

## Diccionario para el análisis

- `participacions.csv`: una fila por persona y carrera. `persoa_id` es el
  pseudónimo; `id_carrera` enlaza con el calendario; `tipo_inscripcion` indica
  el estado de inscripción, y `resultado_cruce` recoge la evidencia del enlace.
  `sexo`, `categoria` y las columnas `puesto_*` contienen los campos separados.
  `tiempo_segundos` expresa la duración en segundos y `estado_tiempo` distingue
  `valido`, `ausente`, `invalido` y `revisar`.
- `carreiras.csv`: una fila por carrera. `id_carrera` es la clave,
  `fecha` es el día de la prueba y `orde` es su posición cronológica.
  Se conservan las columnas de calendario y meteorología de Persona 1.