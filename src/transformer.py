import pandas as pd
from typing import Optional
from src.logger import get_logger

logger = get_logger("transformer")


def _parse_datetime(dt_str: str) -> tuple[Optional[object], Optional[object]]:
    try:
        parts = dt_str.split()
        clean = f"{parts[1]} {parts[2]} {parts[5]} {parts[3]}"
        dt = pd.to_datetime(clean, format="%b %d %Y %H:%M:%S", errors="coerce")
        return dt.date(), dt.time()
    except Exception:
        return None, None


def build_dataframe(records: list[dict]) -> pd.DataFrame:
    logger.info("Construyendo DataFrame desde los registros extraídos.")
    df = pd.DataFrame(records)
    df[["FECHA", "HORA"]] = df["FECHA_HORA_COMPLETA"].apply(
        lambda x: pd.Series(_parse_datetime(x))
    )
    before = len(df)
    df = df.dropna(subset=["FECHA", "HORA"])
    dropped = before - len(df)
    if dropped:
        logger.warning(f"{dropped} filas descartadas por fecha/hora inválida.")
    df = df[["FECHA", "HORA", "MODULO"]].rename(columns={"MODULO": "NÚMERO DE MÓDULO"})
    logger.info(f"DataFrame listo: {len(df)} filas.")
    return df


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Generando resumen de aperturas por módulo.")
    summary = df["NÚMERO DE MÓDULO"].value_counts().reset_index()
    summary.columns = ["Módulo", "Veces abierto"]
    summary = summary.sort_values("Módulo").reset_index(drop=True)
    logger.info(f"Resumen generado: {len(summary)} módulos detectados.")
    return summary