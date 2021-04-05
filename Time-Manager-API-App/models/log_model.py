from db_man import db, db_url
import sqlite3
import app

from models.event_model import  EventModel
from models.task_model import  TaskModel
from models.reminder_model import ReminderModel


class LogModel(db.Model):
    __tablename__ = 'Logs'

    #region SQLAlchemy table columns

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
        db.ForeignKey('Tasks.task_id'),
        nullable = True,
        default = None
    )

    reminder_id = db.Column(
        db.Integer,
        db.ForeignKey('Reminders.reminder_id'),
        nullable = True,
        default = None
    )

    #endregion

    def __init__(self, time_started, time_finished, event_id, task_id, reminder_id):
        self.time_started = time_started
        self.time_finished = time_finished
        self.event_id = event_id
        self.task_id = task_id
        self.reminder_id = reminder_id

    def json(self):
        '''
        This method returns the log object in JSON format.
        '''
        json = {
            'time_started': self.time_started,
            'time_finished': self.time_finished
        }
        if self.event_id:
            event = EventModel.find_by_event_id(self.event_id)
            json['event'] = event.json()
        if self.task_id:
            task = TaskModel.find_by_task_id(self.task_id)
            json['task'] = task.json()
        if self.reminder_id:
            reminder = ReminderModel.find_by_reminder_id(self.reminder_id)
            json['reminder'] = reminder.json()
        return json

    #region DB CRUD mthods
    
    def save_to_db(self):
        '''
        CREATE
        This method saves the current log to the database.
        If the log already exists it will update it.
        '''
        #TODO: implement this method
        pass

    def update_in_db(self):
        '''
        UPDATE
        This method updates the current log in the DB.
        If the log does not exit in the DB it will save it.
        '''
        #TODO: implement this method
        pass

    def delete_from_db(self):
        '''
        This method deletes the currnet log from the database.
        If the log doesn't exist it will do nothing
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_by_task_id(self, task_id):
        '''
        This method searchs the DB for a log with the given task_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass
    
    @classmethod
    def find_by_event_id(self, reminder):
        '''
        This method searchs the DB for a log with the given event_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass
    
    @classmethod
    def find_by_reminder_id(self, reminder):
        '''
        This method searchs the DB for a log with the given reminder_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass
    #endregion