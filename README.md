# Attendance Report

`attendance-report` is a Harbor/Mina task example focused on turning raw attendance data into a reliable report artifact. The task is designed around a practical back-office workflow: attendance records often arrive with ordering issues, missing values, inconsistent labels, and edge cases that only become visible when the final summary is checked carefully. This repository packages that situation as a deterministic benchmark task so an agent must understand the expected outputs, repair the processing logic, and produce repeatable results.

The value of this task is not in a toy calculation, but in the operational discipline it asks for. A good solution should preserve the intended file contract, handle irregular input without breaking valid rows, and write outputs that are stable across repeated runs. It is useful as a reference for building Harbor tasks where CSV-style business data needs validation, aggregation, and clear reporting.

Typical evaluation themes include schema correctness, deterministic ordering, summary accuracy, rejected or incomplete row handling, and clean packaging. The task follows the standard Harbor layout with `instruction.md`, `task.toml`, `environment/`, `solution/`, and `tests/`, making it easy to inspect, run, and adapt for similar reporting workflows.
