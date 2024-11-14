from typing import Dict, List, Optional
from backend.src.errors.custom_error import CustomError


class DatabaseConnectionError(CustomError):
    status_code = 500

    def __init__(self):
        super().__init__(f'Database server is down :(')

    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        return [{"message": self.message}]
