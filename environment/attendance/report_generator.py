from collections import defaultdict
from datetime import datetime, time

from attendance.data_loader import (
    load_attendance,
    load_employees,
    load_leave_requests,
)


def generate_monthly_report(
    employee_file: str,
    leave_file: str,
    attendance_file: str,
    year: int,
    month: int,
) -> list[dict]:
    employees = load_employees(employee_file)
    leave_requests = load_leave_requests(leave_file)
    attendance = load_attendance(attendance_file)

    employee_map = {
        employee.employee_id: employee
        for employee in employees
    }

    attendance = [
        event
        for event in attendance
        if event.timestamp.year == year
        and event.timestamp.month == month
        and event.timestamp.day < 31
    ]

    leave_requests = [
        leave
        for leave in leave_requests
        if leave.date.year == year
        and leave.date.month == month
    ]

    report = {}

    for employee in employees:
        report[employee.employee_id] = {
            "employee_id": employee.employee_id,
            "employee_name": employee.name,
            "worked_hours": 0.0,
            "leave_hours": 0.0,
            "overtime_hours": 0.0,
        }

    events_by_employee_day = defaultdict(list)

    for event in attendance:
        key = (
            event.employee_id,
            event.timestamp.date(),
        )
        events_by_employee_day[key].append(event)

    for (employee_id, work_date), events in events_by_employee_day.items():
        employee = employee_map[employee_id]

        events.sort(key=lambda event: event.timestamp)

        worked_hours = 0.0
        current_clock_in = None

        for event in events:
            if event.event_type == "CLOCK_IN":
                current_clock_in = event.timestamp

            elif event.event_type == "CLOCK_OUT":
                if current_clock_in is None:
                    continue

                worked_hours += (
                    event.timestamp - current_clock_in
                ).total_seconds() / 3600

        report[employee_id]["worked_hours"] += worked_hours

        shift_start = datetime.combine(
            work_date,
            time.fromisoformat(employee.shift_start),
        )

        shift_end = datetime.combine(
            work_date,
            time.fromisoformat(employee.shift_end),
        )

        scheduled_hours = (
            shift_end - shift_start
        ).total_seconds() / 3600

        overtime_hours = max(
            0.0,
            worked_hours - scheduled_hours,
        )

        report[employee_id]["overtime_hours"] += overtime_hours


    for leave in leave_requests:
        report[leave.employee_id]["leave_hours"] += leave.hours
        report[leave.employee_id]["overtime_hours"] = max(
            0.0,
            report[leave.employee_id]["overtime_hours"] - leave.hours,
        )

    return sorted(
        report.values(),
        key=lambda row: row["employee_id"],
    )