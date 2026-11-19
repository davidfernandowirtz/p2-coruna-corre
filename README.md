## As entregas para cada destinatario

A partir da táboa limpa e pseudonimizada (`datos/clean/participacions.csv`), xeráronse tres saídas diferenciadas en `output/` no caderno `04_analisis_base.ipynb`, adaptando o nivel de detalle aos requisitos de privacidade de cada un.

| Destinatario | Ficheiro xerado (`output/`) | Nivel de agregación / privacidade aplicada | Xustificación |
| :--- | :--- | :--- | :--- |
| **Prensa / Web municipal** | `output_prensa_agregado.csv` | **Táboas agregadas** por carreira, sexo e categoría de idade (número de participantes e estatísticos de tempo). | Permite publicar resultados e evolución da participación sen incluír rexistros individuais, pseudónimos nin combinacións que identifiquen a ningunha persoa. |
| **Investigación deportiva** | `output_investigacion_kanon.csv` | **Datos fila a fila** co identificador pseudónimo (`persoa_id`) e **cuasi-identificadores xeneralizados** (agrupación de categorías minoritarias/especiais). Calcúlase e documéntase o nivel de **$k$-anonimato** (`k = [valor_k]`). | Facilita estudos lonxitudinais de rendemento minimizando o risco de reidentificación en grupos pequenos.|
| **Organización do circuíto** | `output_organizacion_gestion.csv` | **Datos operativos de seguimento** por corredor pseudonimizado (`persoa_id`, carreiras disputadas, tipo de inscrición, tempos e postos). | Inclúe unicamente os campos necesarios para auditar a participación e xestionar o circuíto.|

---

## Partes opcionais realizadas

### Opcional 03: Comparativa coa edición anterior (`07_opcional_edicion_anterior.ipynb`)
---

## Presentación

* **Ligazón ao documento de defensa:** [`presentacion/presentacion.pdf`](presentacion/presentacion.pdf).

---

## Reparto do traballo

* **David — Análise exploratoria, saídas por destinatario, Opcional 03 e documentación:**
  * Deseño e execución da análise base de participación, repetición e rendemento (`04_analisis_base.ipynb`), definindo denominadores, universos de abandono e percentiles relativos por sexo/carreira.
  * Xeración e validación de privacidade das tres entregas diferenciadas en `output/` (prensa, investigación con $k$-anonimato e organización).
  * Desenvolvemento completo da **Opcional 03 (Edición anterior)** en `07_opcional_edicion_anterior.ipynb` reutilizando `src/scraping.py` e `src/limpieza.py`.

---

## Uso da IA

* **Ferramentas e finalidade:** Empregouse un asistente de IA como apoio técnico para estruturar funcións de agregación en `pandas`, revisar expresións de cálculo de percentís e $k$-anonimato e organización da documentación
