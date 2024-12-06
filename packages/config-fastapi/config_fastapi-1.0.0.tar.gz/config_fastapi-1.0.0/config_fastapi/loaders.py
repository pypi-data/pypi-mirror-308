import json
from typing import Any, Dict


class JSONConfigLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_config(self) -> Dict[str, Any]:
        with open(self.file_path, "r") as f:
            return json.load(f)
