from typing import Dict, List, Optional
from backend.src.errors.custom_error import CustomError


class BadRequestError(CustomError):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)

    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        return [{"message": self.message}]
