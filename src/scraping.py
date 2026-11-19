
"""Funciones reutilizables para extraer resultados de corunacorre.com.

La lógica es la misma para cualquier edición. Lo que cambia entre ediciones
(idioma de la URL, formato de los enlaces a eventos, nombres de caché y
prefijo de carrera) se pasa como configuración en un EdicionConfig.

Buenas prácticas aplicadas (enunciado 4.3): User-Agent propio, pausa mínima
entre peticiones, caché de bytes en raw_dir y recorrido de todas las páginas
sin saber de antemano cuántas hay.
"""
import re
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://corunacorre.com"
USER_AGENT = "P2-CorunaCorre-BigData-UAC/1.0 (practica academica)"
PAUSA = 1.5  # segundos entre peticiones (mínimo exigido: 1)
TAM_PAGINA = 25
EXCLUIR_CATEGORIAS = (
    "PITUFOS", "BENXAMIN", "ALEVIN", "INFANTIL", "CADETE", "XUVENIL",
)


@dataclass(frozen=True)
class EdicionConfig:
    """Parámetros que cambian de una edición a otra."""

    num_edicion: int
    idioma: str            # "gl" o "es": prefijo de las URLs
    patron_evento: str     # regex con un grupo: id del evento en la página de la edición
    prefijo_carrera: str   # id de carrera: <prefijo>_01, <prefijo>_02...
    raw_dir: Path          # carpeta de caché de esta edición
    cache_eventos: str     # fichero de caché de la página de eventos
    etiqueta_cache: str = ""   # evento_<id>_<etiqueta>_resultados.html
    base_url: str = BASE_URL


def parsear_pagina_resultados(html_bytes, id_carrera, num_pagina):
    """Extrae las filas de la tabla de resultados de una página."""
    soup = BeautifulSoup(html_bytes, "lxml")
    tabla = soup.find("table")
    if not tabla:
        return []

    tbody = tabla.find("tbody")
    filas_html = tbody.find_all("tr") if tbody else tabla.find_all("tr")[1:]

    filas_datos = []
    for tr in filas_html:
        tds = tr.find_all("td")
        if len(tds) < 8:
            continue
        nombre = tds[3].get_text(strip=True)
        apellidos = tds[4].get_text(strip=True)
        filas_datos.append({
            "id_carrera": id_carrera,
            "pagina_origen": num_pagina,
            "puesto": tds[1].get_text(strip=True),
            "dorsal": tds[2].get_text(strip=True),
            "nombre": nombre,
            "apellidos": apellidos,
            "nombre_completo": f"{nombre} {apellidos}".strip(),
            "puesto_sexo": tds[5].get_text(strip=True),
            "puesto_categoria": tds[6].get_text(strip=True),
            "tiempo_oficial": tds[7].get_text(strip=True),
        })
    return filas_datos


class Scraper:
    """Descarga con caché y recorre una edición del circuito."""

    def __init__(self, cfg, pausa=PAUSA, user_agent=USER_AGENT, verbose=True):
        self.cfg = cfg
        self.pausa = max(pausa, 1.0)
        self.headers = {"User-Agent": user_agent}
        self.verbose = verbose
        self.excluidas = []  # eventos sin categoría Absoluta (p. ej. aún no celebrados)
        cfg.raw_dir.mkdir(parents=True, exist_ok=True)

    def descargar_pagina(self, url, nombre_archivo):
        """Devuelve los bytes de la página; si ya está en caché no descarga."""
        ruta = self.cfg.raw_dir / nombre_archivo
        if ruta.exists():
            return ruta.read_bytes()
        if self.verbose:
            print(f"  [DESCARGA] {url}")
        time.sleep(self.pausa)
        resp = requests.get(url, headers=self.headers, timeout=30)
        resp.raise_for_status()
        ruta.write_bytes(resp.content)
        return resp.content

    def descubrir_carreras_absoluta(self):
        """edición -> eventos -> categoría Absoluta (localizada por el texto del enlace)."""
        cfg = self.cfg
        url_eventos = (
            f"{cfg.base_url}/{cfg.idioma}/web/resultado/"
            f"edicion-{cfg.num_edicion}/eventos"
        )
        soup = BeautifulSoup(
            self.descargar_pagina(url_eventos, cfg.cache_eventos), "lxml"
        )

        patron = re.compile(cfg.patron_evento)
        eventos = {}  # id_evento -> texto del primer enlace (orden de aparición)
        for a in soup.find_all("a", href=True):
            m = patron.search(a["href"])
            if m and m.group(1) not in eventos:
                eventos[m.group(1)] = a.get_text(" ", strip=True)

        sufijo = f"_{cfg.etiqueta_cache}" if cfg.etiqueta_cache else ""
        carreras, self.excluidas = [], []
        for id_ev, texto_enlace in eventos.items():
            html_ev = self.descargar_pagina(
                f"{cfg.base_url}/{cfg.idioma}/web/resultado/evento-{id_ev}",
                f"evento_{id_ev}{sufijo}_resultados.html",
            )
            soup_ev = BeautifulSoup(html_ev, "lxml")
            h1 = soup_ev.find("h1")
            nombre = (
                h1.get_text(" ", strip=True).replace("Resultados de", "").strip()
                if h1 else f"Carrera {id_ev}"
            )

            url_abs = None
            for a in soup_ev.find_all("a", href=True):
                texto = a.get_text(" ", strip=True).upper()
                if "ABSOLUTA" in texto and not any(
                    k in texto for k in EXCLUIR_CATEGORIAS
                ):
                    url_abs = a["href"]
                    break

            if url_abs:
                carreras.append({
                    "id_evento": id_ev,
                    "nombre": nombre,            # corto: sirve para emparejar ediciones
                    "nombre_enlace": texto_enlace,  # oficial, con ordinal de edición
                    "url_absoluta": url_abs,
                })
            else:
                self.excluidas.append({"id_evento": id_ev, "nombre": nombre})

        for i, c in enumerate(carreras, start=1):
            c["id_carrera"] = f"{cfg.prefijo_carrera}_{i:02d}"
        return carreras

    def extraer_carrera(self, id_carrera, url_absoluta, tam_pagina=TAM_PAGINA):
        """Recorre todas las páginas de una categoría. Devuelve (DataFrame, nº de páginas).

        Un error de red o de parseo se propaga: no se corta la carrera en silencio.
        """
        filas_carrera, previos, pagina, paginas_ok = [], set(), 1, 0
        while True:
            nombre_raw = f"{id_carrera}_pag_{pagina:02d}.html"
            html = self.descargar_pagina(
                f"{self.cfg.base_url}{url_absoluta}?page={pagina}", nombre_raw
            )
            filas = parsear_pagina_resultados(html, id_carrera, pagina)

            if not filas:  # página vacía: fin
                (self.cfg.raw_dir / nombre_raw).unlink(missing_ok=True)
                break
            actuales = {f["dorsal"] for f in filas}
            if actuales == previos:  # la web repite la última página: fin
                (self.cfg.raw_dir / nombre_raw).unlink(missing_ok=True)
                break

            previos = actuales
            filas_carrera.extend(filas)
            paginas_ok += 1
            if len(filas) < tam_pagina:
                break
            pagina += 1
        return pd.DataFrame(filas_carrera), paginas_ok
