from app.db_man import DBMan
import sqlite3
import app




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