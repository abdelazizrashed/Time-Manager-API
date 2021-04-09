from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .models import ReminderModel, RemindersTimeSlotModel
from .interfaces import ReminderModelInterface, RemindersTimeSlotModelInterface

class ReminderModelService:

    @staticmethod
    def json(reminder: ReminderModel):
        '''
        This method returns the current reminder in JSON format
        '''
        #TODO: modify the json so that it return the color as well as the reminder slots 
        return {
            'reminder_id': reminder.reminder_id,
            'reminder_title': reminder.reminder_title,
            'reminder_description': reminder.reminder_description,
            'is_completed': reminder.is_completed,
            'user_id': reminder.user_id,
            'color_id': reminder.color_id,
            'parent_event_id': reminder.parent_event_id 
        }

    #region DB methods

    @staticmethod
    def create(reminder_attrs: ReminderModelInterface, app: Flask, db: SQLAlchemy) -> ReminderModel:
        '''
        This method saves the current reminder in the database.
        If the reminder already exists it will just update it.
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def update(reminder: ReminderModel, reminder_attrs: ReminderModelInterface, app: Flask, db: SQLAlchemy) -> ReminderModel:
        '''
        This method will update the current reminder in the database.
        If the reminder doesn't exist it will save it 
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def delete(reminder_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method deletes the current reminder from the database.
        If it doesn't exist it will do nothing 
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def retrieve_by_reminder_id(reminder_id: int, app: Flask) -> ReminderModel:
        '''
        This method searches the database for the reminder with the given reminder id.
        If the reminder doesn't exist it will return None
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def retrieve_reminders_by_parent_event_id(parent_event_id: int, app: Flask) -> List[ReminderModel]:
        '''
        This method searches the database for reminder that have the event with the given id as parent and returns them in a list.
        If nothing could be found it will return and empty list.
        '''
        #TODO: implement this method
        pass

    #endregion




class RemindersTimeSlotModelService:


    @staticmethod
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

    @staticmethod
    def save_to_db(self):
        '''
        CREATE
        This method saves the current time slot in the DB if not exists.
        If it exists it will just update it with the current values.
        '''
        #TODO: Implement this method.
        pass

    @staticmethod
    def update_in_db(self):
        '''
        UPDATE
        This method update the current time slot object in the database.
        If it doesn't exist it will save it to the DB.
        '''
        #TODO: Implement this method.
        pass

    @staticmethod
    def delete_from_db(self):
        '''
        DELETE
        This method deletes the current time slot from the DB if exist.
        If it doesn't, it won't do anything. 
        '''
        #TODO: Implement this method.
        pass

    @staticmethod
    def find_slots_by_reminder_id(cls, reminder_id):
        '''
        RETREIVE
        This method searches the DB for the time slots with the given reminder_id and returns a list of them.
        If nothing could be found it will return an empty list.
        '''
        #TODO: Implement this method.
        pass

    #endregion 
