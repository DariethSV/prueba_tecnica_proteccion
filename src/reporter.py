import pandas as pd
from src.transformer import build_dataframe, build_summary
from src.logger import get_logger

logger = get_logger("reporter")


def _write_excel(df: pd.DataFrame, summary: pd.DataFrame, output_file: str) -> None:
    logger.info(f"Escribiendo archivo Excel: {output_file}")
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Registros", index=False)
        summary.to_excel(writer, sheet_name="Resumen", index=False)
    logger.info("Archivo Excel escrito exitosamente.")


def create_excel_report(records: list[dict], output_file: str) -> None:
    if not records:
        logger.warning("No se encontraron datos válidos. El archivo Excel no fue generado.")
        return

    logger.info(f"Iniciando generación del reporte con {len(records)} registros.")
    df = build_dataframe(records)
    summary = build_summary(df)
    _write_excel(df, summary, output_file)
    logger.info("Pipeline finalizado exitosamente.")