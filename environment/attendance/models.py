from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Employee:
    employee_id: str
    name: str
    shift_start: str
    shift_end: str


@dataclass
class AttendanceEvent:
    employee_id: str
    timestamp: datetime
    event_type: str


@dataclass
class LeaveRequest:
    employee_id: str
    date: date
    hours: float

