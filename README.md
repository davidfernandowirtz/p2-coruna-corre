## Las entregas para cada destinatario

A partir de la tabla limpia y pseudonimizada (`datos/clean/participacions.csv`), se generaron tres salidas diferenciadas en `output/` en el cuaderno `04_analisis_base.ipynb`, adaptando el nivel de detalle a los requisitos de privacidad de cada uno.

| Destinatario | Fichero generado (`output/`) | Nivel de agregación / privacidad aplicada | Justificación |
| :--- | :--- | :--- | :--- |
| **Prensa / Web municipal** | `output_prensa_agregado.csv` | **Tablas agregadas** por carrera, sexo y categoría de edad (número de participantes y estadísticos de tiempo). | Permite publicar resultados y evolución de la participación sin incluir registros individuales, pseudónimos ni combinaciones que identifiquen a ninguna persona. |
| **Investigación deportiva** | `output_investigacion_kanon.csv` | **Datos fila a fila** con el identificador pseudónimo (`persoa_id`) y **cuasi-identificadores generalizados** (agrupación de categorías minoritarias/especiales). Se calcula y documenta el nivel de **$k$-anonimato** (`k = [valor_k]`). | Facilita estudios longitudinales de rendimiento minimizando el riesgo de reidentificación en grupos pequeños. |
| **Organización del circuito** | `output_organizacion_gestion.csv` | **Datos operativos de seguimiento** por corredor pseudonimizado (`persoa_id`, carreras disputadas, tipo de inscripción, tiempos y puestos). | Incluye únicamente los campos necesarios para auditar la participación y gestionar el circuito. |

---

## Partes opcionales realizadas

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

---

## Uso de la IA

- **Herramientas y finalidad:** Se empleó un asistente de IA como apoyo técnico para estructurar funciones de agregación en `pandas`, revisar expresiones de cálculo de percentiles y $k$-anonimato, y organización de la documentación.