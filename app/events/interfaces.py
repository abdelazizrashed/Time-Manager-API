from typing import TypedDict



class EventModelInterface(TypedDict, total = False):

    event_id: int
    event_title: str
    event_description: str
    is_completed: int
    user_id: int
    color_id: int
    parent_event_id: int


class EventsTimeSlotsModelInterface(TypedDict, total = False):
    
    time_slot_id: int
    time_from: str
    time_to: str
    location: str
    repeat: str
    reminder: str
    event_id: int