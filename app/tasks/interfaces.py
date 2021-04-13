from typing import TypedDict


class TaskModelInterface(TypedDict, total=False):

    task_id: int
    task_title: str
    task_description: str
    time_from: str
    time_to: str
    time_started: str
    time_finished: str
    is_completed: str
    repeat: str
    reminder: str
    list_id: int
    color_id: int
    user_id: int
    parent_event_id: int
    parent_task_id: int


class TasksListModelInterface(TypedDict, total=False):

    list_id: int
    list_title: str
    user_id: int
