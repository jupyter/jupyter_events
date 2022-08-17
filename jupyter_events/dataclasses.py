from dataclasses import dataclass


@dataclass
class Event:
    schema_id: str
    version: int
    data: dict
