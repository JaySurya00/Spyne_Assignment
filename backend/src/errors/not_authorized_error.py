from typing import Dict, List, Optional
from backend.src.errors.custom_error import CustomError


class NotAuthorizedError(CustomError):
    status_code = 401

    def __init__(self):
        super().__init__("UnAuthorized")

    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        return [{"message": self.message}]
