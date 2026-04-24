from src.parser import parse_log_file
from src.reporter import create_excel_report
from src.logger import get_logger

LOG_FILE = "log_casilleros.txt"
OUTPUT_FILE = "casilleros_log_estructurado.xlsx"

logger = get_logger("main")

if __name__ == "__main__":
    logger.info("=== Inicio del pipeline ===")
    datos = parse_log_file(LOG_FILE)
    create_excel_report(datos, OUTPUT_FILE)
    logger.info("=== Fin del pipeline ===")