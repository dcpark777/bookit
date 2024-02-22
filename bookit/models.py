from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class ResyAuth:
    """
    User account's Resy API Key and Auth Token.
    TODO: 
        1. explain how to find the values via UI.
        2. create function to dynamically retrieve values.
    """
    api_key: str
    auth_token: str

class TableType(Enum):
    DINING = 1
    BAR = 2
    PATIO = 3
    HIGH_TOP = 4
    # COUNTER = 5

@dataclass
class ReservationTimeType:
    time: str
    table_type: str = None # TODO: use TableType enum

@dataclass
class DesiredReservation:
    date: str
    party_size: str # int?
    venue_id: str # int?
    time_types: List[ReservationTimeType] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.time_types, dict):
            self.time_types = [ReservationTimeType(**x) for x in self.time_types]

@dataclass
class AvailableReservationSlot:
    time: str
    table_type: str # TODO: use TableType enum
    config_token: str
    # config_id: str

@dataclass
class BookingInfo:
    payment_method_id: int
    book_token: str

@dataclass
class SnipeTime:
    hours: str # int?
    minutes: str # int?
