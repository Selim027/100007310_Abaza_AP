from dataclasses import dataclass, field
from typing import List

@dataclass
class MarkerProduct:
    serial_number: int
    body_molded: bool = False
    reservoir_filled: bool = False
    tip_inserted: bool = False
    cap_attached: bool = False
    packaged: bool = False
    defective: bool = False
    defect_reason: str = ""
    history: List[str] = field(default_factory=list)

    def add_history(self, message: str) -> None:
        self.history.append(message)
