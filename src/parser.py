import re
import json
from typing import Optional
from src.logger import get_logger

logger = get_logger("parser")

LOG_LINE_FILTER = "name=QUEUE_msg_received"
DATE_PATTERN = re.compile(
    r"([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}\s+[A-Za-z0-9\-\:]+ \d{4})"
)
MSG_BODY_PATTERN = re.compile(r"msg_body=({.*})")


def is_relevant_line(line: str) -> bool:
    return LOG_LINE_FILTER in line


def extract_datetime(line: str) -> Optional[str]:
    match = DATE_PATTERN.search(line)
    return match.group(1) if match else None


def extract_modulo(line: str) -> Optional[str]:
    match = MSG_BODY_PATTERN.search(line)
    if not match:
        return None
    try:
        body = json.loads(match.group(1))
        return body.get("comando", {}).get("payload", {}).get("moduloId")
    except json.JSONDecodeError:
        logger.warning("JSON inválido encontrado, línea omitida.")
        return None


def parse_log_file(log_file_path: str) -> list[dict]:
    logger.info(f"Iniciando lectura del archivo: {log_file_path}")
    seen: set[tuple] = set()
    records: list[dict] = []
    skipped = 0

    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not is_relevant_line(line):
                continue

            datetime_str = extract_datetime(line)
            if not datetime_str:
                skipped += 1
                continue

            modulo = extract_modulo(line)
            if not modulo:
                skipped += 1
                continue

            key = (datetime_str, modulo)
            if key in seen:
                continue

            seen.add(key)
            records.append({"FECHA_HORA_COMPLETA": datetime_str, "MODULO": modulo})

    logger.info(f"Lectura completada: {len(records)} registros únicos extraídos, {skipped} líneas omitidas.")
    return records