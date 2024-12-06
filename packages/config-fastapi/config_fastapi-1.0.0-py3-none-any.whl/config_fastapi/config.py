from typing import Any, Dict, Optional
from .constants import ConfigSource
from .loaders import JSONConfigLoader


class ConfigSection:
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value if not isinstance(value, dict) else ConfigSection(value))

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigSection):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

class Config:
    def __init__(self, source=ConfigSource.JSON, file_path: str = "config_fastapi.json", section: Optional[str] = None):
        # Загрузка конфигурации из указанного источника (по умолчанию JSON)
        if source == ConfigSource.JSON:
            self.loader = JSONConfigLoader(file_path)
        else:
            raise ValueError(f"Unsupported configuration source: {source}")

        full_config = self.loader.load_config()
        self.config_data = ConfigSection(full_config.get(section, full_config))

    def __getattr__(self, item):
        return getattr(self.config_data, item)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self.config_data, key, default)

    def get_logging_config(self) -> Dict[str, Any]:
        logging_config = self.get("logging")
        if isinstance(logging_config, ConfigSection):
            return logging_config.to_dict()
        elif isinstance(logging_config, dict):
            return logging_config
        else:
            raise TypeError("Logging configuration не может быть преобразована в словарь")
