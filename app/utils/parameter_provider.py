import configparser
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "resources" / "config.properties"

class ParameterProvider:
    """Провайдер параметров для чтения конфигурационного файла config.properties."""

    _parameters = None

    @classmethod
    def _load(cls):
        if cls._parameters is None:
            if not CONFIG_PATH.exists():
                raise FileNotFoundError(f"Конфигурационный файл не найден: {CONFIG_PATH}")
            parser = configparser.ConfigParser()
            parser.optionxform = str
            parser.read_string("[config]\n" + CONFIG_PATH.read_text(encoding="utf-8"))
            cls._parameters = dict(parser["config"])
        return cls._parameters

    @classmethod
    def get_required(cls, key):
        """Возвращает значение параметра или выбрасывает ошибку, если его нет."""
        value = cls._load().get(key)
        if value is None:
            raise KeyError(f"Параметр не найден в конфигурации: {key}")
        return value

    @classmethod
    def get(cls, key, default=None):
        """Возвращает значение параметра. Приоритет: переменная окружения > config.properties > default."""
        from_env = os.getenv(key)
        if from_env:
            return from_env
        from_config = cls._load().get(key)
        if from_config:
            return from_config
        return default

    @classmethod
    def get_int(cls, key, default=0):
        """Возвращает целочисленное значение параметра."""
        try:
            return int(cls.get(key, default))
        except (TypeError, ValueError):
            return default