from dataclasses import dataclass


@dataclass
class ModifierData:
    schema_id: str
    version: int
    event_data: dict


@dataclass
class Event:
    schema_id: str
    version: int
    data: dict
