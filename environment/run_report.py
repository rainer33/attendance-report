from attendance.report_generator import generate_monthly_report

report = generate_monthly_report(
    attendance_file="/app/data/attendance.csv",
    employee_file="/app/data/employees.json",
    leave_file="/app/data/leave_requests.csv",
    year=2026,
    month=5,
)

for row in report:
    print(row)