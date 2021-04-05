from db_man import db, db_url
import sqlite3
import app


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

    def __init__(self, reminder_id, reminder_title, reminder_description, in_completed, user_id, color_id, parent_event_id):
        self.reminder_id = reminder_id
        self.reminder_title = reminder_title
        self.reminder_description = reminder_description
        self.is_completed = is_completed
        self.user_id = user_id
        self.color_id = color_id
        self.parent_event_id = parent_event_id

    def json(self):
        '''
        This method returns the current reminder in JSON format
        '''
        #TODO: modify the json so that it return the color as well as the reminder slots 
        return {
            'reminder_id': self.reminder_id,
            'reminder_title': self.reminder_title,
            'reminder_description': self.reminder_description,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'color_id': self.color_id,
            'parent_event_id': self.parent_event_id 
        }

    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current reminder in the database.
        If the reminder already exists it will just update it.
        '''
        #TODO: implement this method
        pass

    def update_in_db(self):
        '''
        This method will update the current reminder in the database.
        If the reminder doesn't exist it will save it 
        '''
        #TODO: implement this method
        pass

    def delete_from_db(self):
        '''
        This method deletes the current reminder from the database.
        If it doesn't exist it will do nothing 
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_by_reminder_id(cls, reminder_id):
        '''
        This method searchs the database for the reminder with the given reminder id.
        If the reminder doesn't exist it will return None
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_reminders_by_parent_event_id(cls, parent_event_id):
        '''
        This method searchs the database for reminder that have the event with the given id as parent and returns them in a list.
        If nothing could be found it will return and empty list.
        '''
        #TODO: implement this method
        pass

    #endregion
