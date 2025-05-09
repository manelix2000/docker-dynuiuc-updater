from dataclasses import dataclass
from typing import Optional

@dataclass
class ApiResponse:
    api: str
    code: int
    msg: str
    timestamp: int
    ip: Optional[str] = None