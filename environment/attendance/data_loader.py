import csv
import json
from datetime import date, datetime

from attendance.models import (
    AttendanceEvent,
    Employee,
    LeaveRequest,
)


def load_employees(employee_file: str) -> list[Employee]:
    with open(employee_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        Employee(
            employee_id=item["employee_id"],
            name=item["name"],
            shift_start=item["shift_start"],
            shift_end=item["shift_end"],
        )
        for item in data
    ]


def load_attendance(attendance_file: str) -> list[AttendanceEvent]:
    events = []

    with open(attendance_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            events.append(
                AttendanceEvent(
                    employee_id=row["employee_id"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    event_type=row["event_type"],
                )
            )

    return events


def load_leave_requests(leave_file: str) -> list[LeaveRequest]:
    requests = []

    with open(leave_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            requests.append(
                LeaveRequest(
                    employee_id=row["employee_id"],
                    date=date.fromisoformat(row["date"]),
                    hours=float(row["hours"]),
                )
            )

    return requests
