## Cómo ejecutar el proyecto

- **Paso 2 — Calidad y limpieza (`02_calidad_limpieza.ipynb`).** Ejecutar
  después de la extracción. Lee los CSV de las carreras en `datos/interim/`
  y genera `datos/interim/resultados_limpios_local.csv`.

- **Paso 4 — Integración y pseudonimización (`03_integracion_pseudonimizacion.ipynb`).**
  Ejecutar cuando estén listos los resultados limpios, el listado de inscritos
  y el calendario base `datos/interim/carreiras_base.csv` que genera el paso 3.
  Configurar antes `CORUNA_HMAC_KEY` con la clave común del equipo en el
  archivo `.env` de la raíz del repositorio. El notebook genera
  `participacions.csv` y `carreiras.csv` en `datos/clean/`, además de
  `enlace_personas_local.csv` en `datos/interim/`.

- **Paso 6 — San Silvestre (`06_opcional_san_silvestre.ipynb`).** Ejecutar
  después del paso 4. Usa el enlace local de personas, el listado de
  inscritos y el calendario final para cruzar la clasificación de
  San Silvestre 2025 con Coruña Corre.

---

## Calidad, limpieza e integración

Se revisaron los valores vacíos, los formatos, los duplicados y los valores imposibles por carrera. Se separaron el sexo, la categoría y sus puestos, y se convirtieron los tiempos a segundos. Se conservaron las 5.390 participaciones de las seis carreras.

| Problema | Dimensión de calidad | Carreras afectadas | Filas | Cómo se detectó | Decisión |
|---|---|---|---:|---|---|
| Puesto por sexo sin dato y código de categoría `NO` | Completitud | Torre de Hércules (3), Matogrande-Xuxán (6), San Pedro de Visma (5) y Volta a Oza (3) | 17 | Aparecía `—` en el puesto por sexo y el patrón `NO-n` en el puesto por categoría. | Se conservaron el código `NO` y el puesto de categoría. Se dejaron vacíos el sexo y su puesto. |
| Tiempos extremos | Validez | Volta a Oza | 3 | Tras convertir los tiempos a segundos, se señalaron los valores iguales o superiores a 7.200 segundos. | Se conservaron los valores con el estado `revisar`. Las dos horas se usaron como umbral provisional de revisión. |

Los controles por carrera no detectaron nombres o dorsales vacíos, dorsales repetidos dentro de una misma prueba ni filas duplicadas. El perfil completo y los recuentos por carrera están en `02_calidad_limpieza.ipynb`.

Para integrar los resultados, se normalizaron los nombres pasando a mayúsculas, quitando tildes y unificando espacios. Se encontraron 315 dorsales asociados a más de un nombre entre carreras. Para identificar a los inscritos se exigió que coincidieran el nombre normalizado y el dorsal con el listado confirmado del circuito.

Se clasificaron 3.833 participaciones como `inscrito_circuito` y 1.458 como `por_prueba` al no encontrar coincidencia en el listado. Quedaron 99 participaciones como `no_resuelto`. En 72 había un candidato por nombre con otro dorsal y en 27 el nombre era ambiguo. Estos casos se conservaron por separado y se registraron en una auditoría local.

Esta decisión reduce el riesgo de unir a dos personas distintas, aunque puede dejar separadas participaciones de una misma persona. Los homónimos y las variantes de escritura siguen siendo limitaciones al contar personas únicas entre carreras.

Los identificadores se generaron mediante HMAC-SHA256 con la clave común `CORUNA_HMAC_KEY`, guardada localmente en `.env`. La exportación conservó las 5.390 filas, sin duplicados en la combinación de pseudónimo y carrera y sin columnas de nombres ni dorsales. Las decisiones de enlace y el diccionario de las tablas finales están en `03_integracion_pseudonimizacion.ipynb`.

---

## Las entregas para cada destinatario

A partir de la tabla limpia y pseudonimizada (`datos/clean/participacions.csv`), se generaron tres salidas diferenciadas en `output/` en el cuaderno `04_analisis_base.ipynb`, adaptando el nivel de detalle a los requisitos de privacidad de cada uno.

| Destinatario | Fichero generado (`output/`) | Nivel de agregación / privacidad aplicada | Justificación |
| :--- | :--- | :--- | :--- |
| **Prensa / Web municipal** | `output_prensa_agregado.csv` | **Tablas agregadas** por carrera, sexo y categoría de edad (número de participantes y estadísticos de tiempo). | Permite publicar resultados y evolución de la participación sin incluir registros individuales, pseudónimos ni combinaciones que identifiquen a ninguna persona. |
| **Investigación deportiva** | `output_investigacion_kanon.csv` | **Datos fila a fila** con el identificador pseudónimo (`persoa_id`) y **cuasi-identificadores generalizados** (agrupación de categorías minoritarias/especiales). Se calcula y documenta el nivel de **$k$-anonimato** (`k = [valor_k]`). | Facilita estudios longitudinales de rendimiento minimizando el riesgo de reidentificación en grupos pequeños. |
| **Organización del circuito** | `output_organizacion_gestion.csv` | **Datos operativos de seguimiento** por corredor pseudonimizado (`persoa_id`, carreras disputadas, tipo de inscripción, tiempos y puestos). | Incluye únicamente los campos necesarios para auditar la participación y gestionar el circuito. |

---

## Partes opcionales realizadas

### Opcional 02: San Silvestre 2025 (`06_opcional_san_silvestre.ipynb`)

Se usó la [clasificación oficial de la Carrera Principal de San Silvestre 2025](https://sansilvestrecoruna.com/gl/web/resultado/competicion-16683), que agrupa Absoluta y Andaina. La prueba se celebró el 31 de diciembre de 2025 y la clasificación se descargó el 18 de noviembre de 2026. Se siguió el enlace de página siguiente hasta recorrer las 215 páginas, con un agente de usuario propio, una pausa entre peticiones y caché local de los HTML.

Se analizaron 5.366 resultados. Como las dos fuentes carecen de un identificador común, se cruzaron mediante el nombre normalizado y HMAC con la clave del equipo. Se encontraron 697 coincidencias con participantes de carreras posteriores de Coruña Corre y 527 con el listado de inscritos al circuito. Se excluyeron 41 registros del cruce por ambigüedad.

Los dos grupos pueden solaparse. Las coincidencias por nombre son aproximadas, ya que los homónimos y las variantes de escritura pueden afectar al enlace. El notebook incluye el desglose por sexo y categoría de los dos grupos.

### Opcional 03: Comparativa con la edición anterior (`07_opcional_edicion_anterior.ipynb`)

---

## Presentación

- **Enlace al documento de defensa:** [`presentacion/presentacion.pdf`](presentacion/presentacion.pdf).

---

## Reparto del trabajo

- **David — Análisis exploratorio, salidas por destinatario, Opcional 03 y documentación:**
  - Diseño y ejecución del análisis base de participación, repetición y rendimiento (`04_analisis_base.ipynb`), definiendo denominadores, universos de abandono y percentiles relativos por sexo/carrera.
  - Generación y validación de privacidad de las tres entregas diferenciadas en `output/` (prensa, investigación con $k$-anonimato y organización).
  - Desarrollo completo de la **Opcional 03 (Edición anterior)** en `07_opcional_edicion_anterior.ipynb` reutilizando `src/scraping.py` y `src/limpieza.py`.

- **Javier — Calidad, limpieza, integración y Opcional 02:**
  - Preparación y ejecución de los notebooks `02_calidad_limpieza.ipynb` y `03_integracion_pseudonimizacion.ipynb`, con perfil de calidad por carrera, documentación de incidencias y auditoría del enlace de personas.
  - Generación de `participacions.csv` y `carreiras.csv` para el análisis y elaboración del diccionario de datos ([issue #5](https://github.com/davidfernandowirtz/p2-coruna-corre/issues/5), [PR #9](https://github.com/davidfernandowirtz/p2-coruna-corre/pull/9)).
  - Descarga y cruce de los resultados de la **Opcional 02 (San Silvestre)** con los de Coruña Corre en `06_opcional_san_silvestre.ipynb` ([issue #6](https://github.com/davidfernandowirtz/p2-coruna-corre/issues/6), [PR #10](https://github.com/davidfernandowirtz/p2-coruna-corre/pull/10)).

---

## Uso de la IA

- **Herramientas y finalidad:** Se empleó un asistente de IA como apoyo técnico para estructurar funciones de agregación en `pandas`, revisar expresiones de cálculo de percentiles y $k$-anonimato, y organización de la documentación.