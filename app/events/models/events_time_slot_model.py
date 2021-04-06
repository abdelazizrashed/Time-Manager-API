from app.db_man import DBMan
import sqlite3
import app


class EventsTimeSlotModel(DBMan.db.Model):
    __tablename__ = 'EventsTimeSlots'

    
    #region SQLAlchemy table columns
    time_slot_id = DBMan.db.Column(
        DBMan.db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    time_form = DBMan.db.Column(
        DBMan.db.String(100),
        nullable = False
    )

    time_to = DBMan.db.Column(
        DBMan.db.String(100),
        nullable = False
    )

    location = DBMan.db.Column(
        DBMan.db.String(100),
        nullable = True,
        default = None
    )

    repeat = DBMan.db.Column(
        DBMan.db.String(100),
        nullable = True,
        default = None
    )

    reminder = DBMan.db.Column(
        DBMan.db.String(100),
        nullable = True,
        default = None
    )

    event_id = DBMan.db.Column(
        DBMan.db.Integer,
        DBMan.db.ForeignKey('Events.event_id'),
        nullable = False
    )

    #endregion

    def __init__(self, time_from, time_to, location, repeat, reminder, event_id):
        self.time_form = time_from
        self.time_to = time_to
        self.location = location
        self.repeat = repeat
        self.remider = reminder
        self.event_id = event_id

    def json(self):
        '''
        This method return the object in JSON format
        '''
        return {
            'time_from': self.time_form,
            'time_to': self.time_to,
            'location': self.location,
            'repeat': self.repeat,
            'reminder': self.reminder,
            'event_id': self.event_id
        }

    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current time slot into the database.
        If the time slot already exists in the database it will update it.
        '''
        #TODO: impletment the method
        pass

    def update_in_db(self):
        '''
        This method updates the current time slot in the database.
        If the time slot doesn't exist in the database it will be created.
        '''
        #TODO: impletment the method
        pass

    def delete_from_db(self):
        '''
        This method deletes the current time slot from the database.
        If the the time slot doesn't exist in the database it will do nothing.
        '''
        #TODO: impletment the method
        pass

    @classmethod
    def find_slots_by_event_id(cls, event_id):
        '''
        This method searchs the database for the time slots that belong to the event with the given event_id
        and returns a list of the time slots
        '''
        #TODO: impletment the method
        pass

    #endregion