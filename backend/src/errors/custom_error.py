from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class CustomError(ABC, Exception):
    status_code: int

    def __init__(self, message: str):
        super().__init__()
        self.message = message  # Store the message for later use

    @abstractmethod
    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        pass  # Subclasses must override this method
