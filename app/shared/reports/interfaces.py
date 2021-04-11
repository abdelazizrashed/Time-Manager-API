from typing import TypedDict

class ReportInterface(TypedDict, total = False):

    report_id: int
    time_started: str
    time_finished: str
    event_id: int
    task_id: int
    reminder_id: int
    user_id: int