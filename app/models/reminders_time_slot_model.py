from db_man import db, db_url
import sqlite3
import app


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

    def __init__(self, time, repeat, reminder, reminder_id):
        self.time = time
        self.repeat = repeat
        self.reminder_id = reminder_id

    def json(self):
        '''
        This method returns the current reminders time slot object in JSON format.
        '''
        return {
            'time': self.time,
            'repeat': self.repeat,
            'reminder': self.reminder,
            'reminder_id': self.reminder_id
        }
    
    #region DB CRUD methods

    def save_to_db(self):
        '''
        CREATE
        This method saves the current time slot in the DB if not exists.
        If it exists it will just update it with the current values.
        '''
        #TODO: Implement this method.
        pass

    def update_in_db(self):
        '''
        UPDATE
        This method update the current time slot object in the database.
        If it doesn't exist it will save it to the DB.
        '''
        #TODO: Implement this method.
        pass

    def delete_from_db(self):
        '''
        DELETE
        This method deletes the current time slot from the DB if exist.
        If it doesn't, it won't do anything. 
        '''
        #TODO: Implement this method.
        pass

    @classmethod
    def find_slots_by_reminder_id(cls, reminder_id):
        '''
        RETREIVE
        This method searchs the DB for the time slots with the given reminder_id and returns a list of them.
        If nothing could be found it will return an empty list.
        '''
        #TODO: Implement this method.
        pass

    #endregion 
