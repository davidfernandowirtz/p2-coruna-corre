
"""Limpieza de resultados. Replica la lógica del notebook 02 (Persona 2)
para que todas las ediciones se limpien con los mismos criterios."""
import pandas as pd

UMBRAL_REVISAR_SEGUNDOS = 7200  # criterio provisional del notebook 02


def limpiar_resultados(res):
    """Separa puestos compuestos, convierte tiempos a segundos y marca su estado.

    res: DataFrame con columnas de texto puesto, puesto_sexo, puesto_categoria
    y tiempo_oficial (leído con dtype=str y keep_default_na=False).
    No elimina filas: devuelve una columna por cada dato separado.
    """
    puesto = res["puesto"].str.strip()
    sexo = res["puesto_sexo"].str.strip().str.upper()
    categoria = (
        res["puesto_categoria"].str.strip().str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    tiempo = res["tiempo_oficial"].str.strip()

    out = res.copy()
    out["puesto_general"] = puesto.where(
        puesto.str.fullmatch(r"[1-9]\d*")
    ).astype("Int64")

    # M-3 -> sexo M, puesto 3
    partes_sexo = sexo.str.extract(
        r"^(?P<sexo>[MF])\s*-\s*(?P<puesto_por_sexo>[1-9]\d*)$"
    )
    out["sexo"] = partes_sexo["sexo"].astype("string")
    out["puesto_por_sexo"] = partes_sexo["puesto_por_sexo"].astype("Int64")

    # MS2M-1 -> categoría MS2, sexo M, puesto 1
    partes_cat = categoria.str.extract(
        r"^(?P<categoria>[A-Z0-9]+)(?P<sexo_categoria>[MF])"
        r"\s*-\s*(?P<puesto_por_categoria>[1-9]\d*)$"
    )
    out["categoria"] = partes_cat["categoria"].astype("string")
    out["sexo_categoria"] = partes_cat["sexo_categoria"].astype("string")
    out["puesto_por_categoria"] = partes_cat["puesto_por_categoria"].astype("Int64")

    # NO-n: se conserva el código de origen y su puesto de categoría
    puesto_no = categoria.str.extract(r"^NO\s*-\s*([1-9]\d*)$", expand=False)
    es_no = puesto_no.notna()
    out.loc[es_no, "categoria"] = "NO"
    out.loc[es_no, "puesto_por_categoria"] = puesto_no[es_no].astype("Int64")

    # MM:SS o HH:MM:SS -> segundos, con estado en vez de borrar
    partes_t = tiempo.str.extract(
        r"^(?:(?P<horas>\d+):(?=[0-5]\d:))?"
        r"(?P<minutos>\d+):(?P<segundos>[0-5]\d)$"
    ).astype("Int64")
    segundos = (
        partes_t["horas"].fillna(0) * 3600
        + partes_t["minutos"] * 60
        + partes_t["segundos"]
    )
    positivo = segundos.gt(0).fillna(False)
    out["tiempo_segundos"] = segundos.where(positivo)
    out["estado_tiempo"] = "invalido"
    out.loc[tiempo.eq(""), "estado_tiempo"] = "ausente"
    out.loc[positivo, "estado_tiempo"] = "valido"
    out.loc[segundos.ge(UMBRAL_REVISAR_SEGUNDOS).fillna(False), "estado_tiempo"] = "revisar"

    assert len(out) == len(res), "La limpieza no debe perder ni duplicar filas"
    return out
