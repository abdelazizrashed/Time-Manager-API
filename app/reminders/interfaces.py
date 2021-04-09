from typing import TypedDict



class ReminderModelInterface(TypedDict, total = False):


    reminder_id: int
    reminder_title: str
    reminder_description: str
    is_completed: int
    user_id: int
    color_id: int
    parent_event_id: int



class RemindersTimeSlotModelInterface(TypedDict, total = False):


    time: str
    repeat: str
    reminder: str
    reminder_id: int