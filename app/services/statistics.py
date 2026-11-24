import csv
import io

from app.constants import messages
from app.exceptions.statistics_error import StatisticsError
from app.utils.logger import get_logger

logger = get_logger(__name__)

def calculate_statistics(text: str, column: str) -> dict:
    if text.strip() == "":
        raise StatisticsError(messages.EMPTY_FILE)

    rows = list(csv.DictReader(io.StringIO(text)))
    if len(rows) == 0:
        raise StatisticsError(messages.NO_DATA)
    if column not in rows[0]:
        raise StatisticsError(messages.COLUMN_NOT_FOUND.format(column=column))

    values = []
    for row in rows:
        try:
            values.append(float(row[column]))
        except (TypeError, ValueError):
            raise StatisticsError(messages.INVALID_VALUE.format(value=row[column], column=column))

    logger.info("Прочитано значений в столбце '%s': %d", column, len(values))
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 2),
    }