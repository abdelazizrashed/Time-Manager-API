from ..db_man.service import  db
from .interfaces import ReportInterface


class ReportModel(db.Model):
    __tablename__ = "Reports"


    report_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    time_started = db.Column(
        db.String(100),
        nullable = False
    )

    time_finished = db.Column(
        db.String(100),
        nullable = False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = True,
        default = None
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = True,
        default = None
    )

    reminder_id = db.Column(
        db.Integer,
        db.ForeignKey('Reminders.reminder_id'),
        nullable = True,
        default = None
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('Users.user_id'),
        nullable = False
    )


    def update(self, report_attrs: ReportInterface):

        for key, value in report_attrs.items():
            setattr(self, key, value)
        
        return self