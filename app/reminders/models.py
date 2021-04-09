from ..shared.db_man.service import db
from .interfaces import ReminderModelInterface, RemindersTimeSlotModelInterface


class ReminderModel(db.Model):
    __tablename__ = 'Reminders'

    #region SQLAlchemy table columns

    reminder_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    reminder_title = db.Column(
        db.String(50),
        nullable = False
    )

    reminder_description = db.Column(
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

    def update(self, reminder_attrs: ReminderModelInterface):

        for key, value in reminder_attrs.keys():
            setattr(self, key, value)

    


class RemindersTimeSlotModel(db.Model):
    __tablename__ = 'RemindersTimeSlots'

    #region SQLAlchemy table columns

    time = db.Column(
        db.String(100),
        nullable = False
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

    reminder_id = db.Column(
        db.Integer,
        db.ForeignKey('Reminders.reminder_id'),
        nullable = False
    )

    #endregion

    def update(self, time_slot_attrs: RemindersTimeSlotModelInterface):

        for key, value in time_slot_attrs.keys():
            setattr(self, key, value)