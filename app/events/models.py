from app.shared.db_man.service import db
from .interfaces import EventModelInterface, EventsTimeSlotsModelInterface


class EventModel(db.Model):

    __tablename__ = 'Events'

    #region SQLAlchemy table columns

    event_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    event_title = db.Column(
        db.String(50),
        nullable = False
    )

    event_description = db.Column(
        db.String(250),
        nullable = True,
        default = None
    )

    is_completed = db.Column(
        db.Boolean,
        nullable = True,
        default = 0
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('Users.user_id'),
        nullable = False
    )

    color_id = db.Column(
        db.Integer,
        db.ForeignKey('Colors.color_id'),
        nullable = False
    )

    parent_event_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = True,
        default = None
    )
    #endregion

    def update(self, updates: EventModelInterface):
        
        for key, value in updates.items():
            setattr(self, key, value)
        return self


class EventsTimeSlotModel(db.Model):
    __tablename__ = 'EventsTimeSlots'

    
    #region SQLAlchemy table columns
    time_slot_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    time_form = db.Column(
        db.String(100),
        nullable = False
    )

    time_to = db.Column(
        db.String(100),
        nullable = False
    )

    location = db.Column(
        db.String(100),
        nullable = True,
        default = None
    )

    repeat = db.Column(
        db.String(100),
        nullable = True,
        default = None
    )

    reminder = db.Column(
        db.String(100),
        nullable = True,
        default = None
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = False
    )

    #endregion

    def update(self, updates: EventsTimeSlotsModelInterface):
        
        for key, value in updates.items():
            setattr(self, key, value)
        return self