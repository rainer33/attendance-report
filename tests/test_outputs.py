from attendance.report_generator import generate_monthly_report


def test_generate_monthly_report():
    """Verify monthly attendance report generation."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    assert isinstance(report, list)

    assert len(report) == 6

    ids = [row["employee_id"] for row in report]
    assert len(ids) == len(set(ids))

    employee_ids = {row["employee_id"] for row in report}

    assert employee_ids == {
        "EMP001",
        "EMP002",
        "EMP003",
        "EMP004",
        "EMP005",
        "EMP006",
    }
    assert [row["employee_id"] for row in report] == [
        "EMP001",
        "EMP002",
        "EMP003",
        "EMP004",
        "EMP005",
        "EMP006",
    ]
    required_fields = {
        "employee_id",
        "employee_name",
        "worked_hours",
        "leave_hours",
        "overtime_hours",
    }

    for row in report:
        assert required_fields.issubset(row.keys())

        assert isinstance(row["employee_id"], str)
        assert isinstance(row["employee_name"], str)

        assert isinstance(row["worked_hours"], (int, float))
        assert isinstance(row["leave_hours"], (int, float))
        assert isinstance(row["overtime_hours"], (int, float))

        assert row["worked_hours"] >= 0
        assert row["leave_hours"] >= 0
        assert row["overtime_hours"] >= 0


def test_duplicate_attendance_events_are_ignored():
    """Verify that duplicate attendance events are ignored."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP001"
    )

    assert employee["worked_hours"] == 17.0
    assert employee["overtime_hours"] == 1.0


def test_leave_does_not_reduce_overtime():
    """Verify that leave does not reduce overtime hours."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP003"
    )

    assert employee["worked_hours"] == 16.0
    assert employee["leave_hours"] == 12.0
    assert employee["overtime_hours"] == 4.0


def test_last_day_of_month_is_included():
    """Verify that the last day of the month is included in the report."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP002"
    )

    assert employee["worked_hours"] == 8.0


def test_emp004_report_values():
    """Verify EMP004 computed values are correct."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP004"
    )

    assert employee["worked_hours"] == 8.0
    assert employee["overtime_hours"] == 0.0
    assert employee["leave_hours"] == 0.0


def test_orphaned_clock_in_is_ignored():
    """Verify that a CLOCK_IN with no matching CLOCK_OUT does not count toward worked hours."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP005"
    )

    assert employee["worked_hours"] == 8.0
    assert employee["overtime_hours"] == 0.0
    assert employee["leave_hours"] == 0.0


def test_employee_without_attendance_in_report():
    """Verify that employees with no attendance records still appear in the report with zero values."""
    report = generate_monthly_report(
        attendance_file="/app/data/attendance.csv",
        employee_file="/app/data/employees.json",
        leave_file="/app/data/leave_requests.csv",
        year=2026,
        month=5,
    )

    employee = next(
        row for row in report
        if row["employee_id"] == "EMP006"
    )

    assert employee["worked_hours"] == 0.0
    assert employee["overtime_hours"] == 0.0
    assert employee["leave_hours"] == 0.0