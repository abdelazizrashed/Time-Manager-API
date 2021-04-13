from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .models import ReminderModel, RemindersTimeSlotModel
from .interfaces import ReminderModelInterface, RemindersTimeSlotModelInterface
from ..shared.db_man.service import DBMan

class ReminderModelService:

    @staticmethod
    def json(reminder: ReminderModel, app: Flask):
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
            'parent_event_id': reminder.parent_event_id,
            'time_slots': [RemindersTimeSlotModelService.json(reminder) for reminder in RemindersTimeSlotModelService.retrieve_slots_by_reminder_id(reminder.reminder_id, app)]
        }

    #region DB methods

    @staticmethod
    def create(reminder_attrs: ReminderModelInterface, app: Flask, db: SQLAlchemy) -> ReminderModel:
        '''
        This method saves the current reminder in the database.
        If the reminder already exists it will just update it.
        '''
        new_reminder: ReminderModel = ReminderModel()
        new_reminder.update(reminder_attrs)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO Reminders(
                        reminder_title,
                        reminder_description,
                        is_complete,
                        user_id,
                        color_id,
                        parent_event_id
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
            rows_n_rowid = list(DBMan.execute_sql_query(app, query,(
                new_reminder.reminder_title, 
                new_reminder.reminder_description,
                new_reminder.is_completed,
                new_reminder.user_id,
                new_reminder.color_id,
                new_reminder.parent_event_id
                ) 
            ))
            return new_reminder.update(dict(reminder_id = rows_n_rowid[0]))
        else:
            db.session.add(new_reminder)
            db.session.commit()
            return new_reminder

    @staticmethod
    def update(reminder: ReminderModel, updates: ReminderModelInterface, app: Flask, db: SQLAlchemy) -> ReminderModel:
        '''
        This method will update the current reminder in the database.
        If the reminder doesn't exist it will save it 
        '''
        reminder.update(updates)
        if not ReminderModelService.retrieve_by_reminder_id(reminder.reminder_id):
            return ReminderModelService.create(updates, app, db)
        if app.config['DEBUG']:
            query = """
                    UPDATE Reminders
                    SET reminder_title = ?, reminder_description = ?, is_completed = ?, user_id = ?, color_id = ?, parent_event_id = ?
                    WHERE reminder_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (
                reminder.reminder_title, 
                reminder.reminder_description,
                reminder.is_completed,
                reminder.user_id,
                reminder.color_id,
                reminder.parent_event_id,
                reminder.reminder_id
                )
            )
        else:
            db.session.commit()
        return reminder

    @staticmethod
    def delete(reminder_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method deletes the current reminder from the database.
        If it doesn't exist it will do nothing 
        '''
        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(reminder_id)
        if reminder:

            RemindersTimeSlotModelService.delete_all_by_reminder_id(reminder_id, app, db)

            if app.config['DEBUG'] or app.config['TESTING']:
                
                query = 'DELETE FROM Reminders WHERE reminder_id = ?;'
                DBMan.execute_sql_query(app, query, (reminder_id,))
                
            else:
                db.session.delete(reminder)
                db.session.commit()
            return reminder_id
        return None

    @staticmethod
    def retrieve_by_reminder_id(reminder_id: int, app: Flask) -> ReminderModel:
        '''
        This method searches the database for the reminder with the given reminder id.
        If the reminder doesn't exist it will return None
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Reminders WHERE reminder_id = ?;'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (reminder_id,)))
            reminder: ReminderModel = ReminderModel()
            for row in rows_n_rowid[1]:
                return reminder.update(dict(
                    reminder_id = row[0],
                    reminder_title = row[1],
                    reminder_description = row[2],
                    is_complete = row[3],
                    user_id = row[4],
                    color_id = row[5],
                    parent_event_id = row[6]
                ))
            return None

        else:
            return ReminderModel.query.filter_by(reminder_id = reminder_id).first()

    @staticmethod
    def retrieve_reminders_by_parent_event_id(parent_event_id: int, app: Flask) -> List[ReminderModel]:
        '''
        This method searches the database for reminder that have the event with the given id as parent and returns them in a list.
        If nothing could be found it will return and empty list.
        '''
        #TODO: implement this method
        raise NotImplementedError

    @staticmethod
    def retrieve_reminders_by_user_id(user_id: int, app: Flask) -> List[ReminderModel]:
        '''
        This method return a list of all the reminder that belong to a specific use.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Reminders WHERE user_id = ?'
            rows = DBMan.execute_sql_query(app, query, (user_id,))

            reminders: List[ReminderModel] = []
            for row in rows:
                event: EventModel = ReminderModel()
                event.update(dict(
                    reminder_id = row[0],
                    reminder_title = row[1],
                    reminder_description = row[2],
                    is_complete = row[3],
                    user_id = row[4],
                    color_id = row[5],
                    parent_event_id = row[6]
                ))
                reminders.append(event)

            return reminders
        else:
            return ReminderModel.query.filter_by(user_id = user_id).all()
    #endregion




class RemindersTimeSlotModelService:


    @staticmethod
    def json(time_slot: RemindersTimeSlotModel):
        '''
        This method returns the current reminders time slot object in JSON format.
        '''
        return {
            'time': time_slot.time,
            'repeat': time_slot.repeat,
            'reminder': time_slot.reminder,
            'reminder_id': time_slot.reminder_id
        }
    
    #region DB CRUD methods

    @staticmethod
    def create(time_slot_attrs: RemindersTimeSlotModelInterface, app: Flask, db: SQLAlchemy) -> RemindersTimeSlotModel:
        '''
        CREATE
        This method saves the current time slot in the DB if not exists.
        If it exists it will just update it with the current values.
        '''
        new_time_slot: RemindersTimeSlotModel = RemindersTimeSlotModel()
        new_time_slot.update(time_slot_attrs)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO ReminderTimeSlots(
                        time, 
                        repeat,
                        reminder,
                        reminder_id
                    ) VALUES (?, ?, ?, ?);
                    """
            rows_n_rowid = list(DBMan.execute_sql_query(app, query,(
                new_time_slot.time,
                new_time_slot.repeat,
                new_time_slot.reminder,
                new_time_slot.reminder_id
                ) 
            ))
            return new_time_slot.update(dict(time_slot_id = rows_n_rowid[0]))
        else:
            db.session.add(new_time_slot)
            db.session.commit()
            return new_time_slot

    @staticmethod
    def update(time_slot: RemindersTimeSlotModel, updates: RemindersTimeSlotModelInterface, app: Flask, db: SQLAlchemy) -> RemindersTimeSlotModel:
        '''
        UPDATE
        This method update the current time slot object in the database.
        If it doesn't exist it will save it to the DB.
        '''
        #TODO: implement this method
        raise NotImplementedError

    @staticmethod
    def delete_all_by_reminder_id(reminder_id: int, app: Flask, db: SQLAlchemy):
        '''
        This method deletes all the time slots that belong to a specific reminder.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = '''
                    DELETE FROM RemindersTimeSlots WHERE reminder_id = ?;
                    '''
            DBMan.execute_sql_query(app, query, (reminder_id,))
        else:
            for time_slot in RemindersTimeSlotModelService.retrieve_slots_by_reminder_id(reminder_id, app):
                db.session.delete(time_slot)
                db.session.commit()

    @staticmethod
    def retrieve_slots_by_reminder_id(reminder_id: int, app: Flask) -> List[RemindersTimeSlotModel]:
        '''
        RETREIVE
        This method searches the DB for the time slots with the given reminder_id and returns a list of them.
        If nothing could be found it will return an empty list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM RemindersTimeSlots WHERE reminder_id = ?'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (reminder_id,)))

            time_slots: List[RemindersTimeSlotModel] = []
            for row in rows_n_rowid[1]:
                time_slot: RemindersTimeSlotModel = RemindersTimeSlotModel()
                time_slot.update(dict(
                    time = row[0],
                    repeat = row[3],
                    reminder = row[4],
                    reminder_id = row[5]
                ))
                time_slots.append(time_slot)

            return time_slots
        else:
            return RemindersTimeSlotModel.query.filter_by(reminder_id = reminder_id).all()

    #endregion 
