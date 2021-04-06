from pytest import  fixture
from app.models.event_model import  EventModel

@fixture
def event_model() -> EventModel:
    return EventModel(
        1,
        'first class',
        'new_class',
        0,
        1,
        1,
        1
    )

def test_EventModel_create(event_model: EventModel):
    assert event_model