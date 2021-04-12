from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from ..shared.db_man.service import DBMan
from .models import EventModel, EventsTimeSlotModel
from .interfaces import EventModelInterface, EventsTimeSlotsModelInterface


class EventModelService:

    @staticmethod
    def json(event: EventModel, app: Flask):
        '''
        This method return the object in JSON format
        '''
        #TODO: change it so that it return the JSON of the time slots as well as the JSON of the color
        return {
            'event_id': event.event_id,
            'event_title': event.event_title,
            'event_description': event.event_description,
            'is_completed': event.is_completed,
            'user_id': event.user_id,
            'color_id': event.color_id,
            'parent_event_id': event.parent_event_id, 
            'time_slots': [EventsTimeSlotModelService.json(time_slot) for time_slot in EventsTimeSlotModelService.retrieve_slots_by_event_id(event.event_id, app)]
        }
    
    #region DB CRUD methods
    
    @staticmethod
    def create(event_attrs: EventModelInterface, app: Flask, db: SQLAlchemy) -> EventModel:
        '''
        This method saves the current event to the database.
        If the event already exists it will just update it.
        '''
        new_event: EventModel = EventModel()
        new_event.update(event_attrs)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO Events VALUES (NULL, ?, ?, ?, ?, ?, ?);
                    """
            DBMan.execute_sql_query(app, query,(
                new_event.event_title, 
                new_event.event_description,
                new_event.is_completed,
                new_event.user_id,
                new_event.color_id,
                new_event.parent_event_id
                ) 
            )
        else:
            db.session.add(new_event)
            db.session.commit()
        return new_event

    @staticmethod
    def update(event: EventModel, updates: EventModelInterface, app: Flask, db: SQLAlchemy) -> EventModel: 
        '''
        This method update the current event in the database.
        If the event already exists it will save it to the database.
        '''
        event.update(updates)
        if not EventModelService.retrieve_by_event_id(event.event_id):
            return EventModelService.create(updates, app, db)
        if app.config['DEBUG']:
            query = """
                    UPDATE Events
                    SET event_title = ?, event_description = ?, is_completed = ?, user_id = ?, color_id = ?, parent_event_id = ?
                    WHERE event_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (
                event.event_title, 
                event.event_description,
                event.is_completed,
                event.user_id,
                event.color_id,
                event.parent_event_id,
                event.event_id
                )
            )
        else:
            db.session.commit()
        return event

    @staticmethod
    def delete(event_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method will delete the current event from the database only if it exists.
        '''
        event: EventModel = EventModelService.retrieve_by_event_id(event_id)
        if event:
            #TODO: delete all tasks that have this event as its parent

            events = EventModelService.retrieve_events_by_parent_id(event_id)
            for e in events:

                EventModelService.delete(e.event_id, app, db)

            EventsTimeSlotModelService.delete_all_by_event_id(event_id, app, db)

            if app.config['DEBUG'] or app.config['TESTING']:
                
                query = 'DELETE FROM Events WHERE event_id = ?;'
                DBMan.execute_sql_query(app, query, (event_id, ))
                
            else:
                db.session.delete(event)
                db.session.commit()
            return event_id
        return None

    
    @staticmethod
    def retrieve_by_event_id(event_id: int, app: Flask) -> EventModel:
        '''
        This method searches the database for an event with the given event id.
        If the event does not exist it will return None.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Events WHERE event_id = ?;'
            rows = DBMan.execute_sql_query(app, query, (event_id,))
            event: EventModel = EventModel()
            for row in rows:
                return event.update(dict(
                    event_id = row[0],
                    event_title = row[1],
                    event_description = row[2],
                    is_complete = row[3],
                    user_id = row[4],
                    color_id = row[5],
                    parent_event_id = row[6]
                ))
            return None

        else:
            return EventModel.query.filter_by(event_id = event_id).first()

    
    @staticmethod
    def retrieve_events_by_parent_id(parent_event_id: int, app: Flask) -> List[EventModel]:
        '''
        This method finds events by its parent event id and return a list of event that match.
        If nothing found it will return and empty list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Events WHERE parent_event_id = ?'
            rows = DBMan.execute_sql_query(app, query, (parent_event_id,))

            events: List[EventModel] = []
            for row in rows:
                event: EventModel = EventModel()
                event.update(dict(
                    event_id = row[0],
                    event_title = row[1],
                    event_description = row[2],
                    is_complete = row[3],
                    user_id = row[4],
                    color_id = row[5],
                    parent_event_id = row[6]
                ))
                events.append(event)

            return events
        else:
            return EventModel.query.filter_by(parent_event_id = parent_event_id).all()

    
    @staticmethod
    def retrieve_events_by_user_id(user_id: int, app: Flask) ->List[EventModel]:
        '''
        This method returns a list of all the events that belong to a user whom user_id is provided.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Events WHERE user_id = ?'
            rows = DBMan.execute_sql_query(app, query, (user_id,))

            events: List[EventModel] = []
            for row in rows:
                event: EventModel = EventModel()
                event.update(dict(
                    event_id = row[0],
                    event_title = row[1],
                    event_description = row[2],
                    is_complete = row[3],
                    user_id = row[4],
                    color_id = row[5],
                    parent_event_id = row[6]
                ))
                events.append(event)

            return events
        else:
            return EventModel.query.filter_by(user_id = user_id).all()
    #endregion

class EventsTimeSlotModelService:

    @staticmethod
    def json(time_slot: EventsTimeSlotModel):
        '''
        This method return the object in JSON format
        '''
        return {
            'time_from': time_slot.time_form,
            'time_to': time_slot.time_to,
            'location': time_slot.location,
            'repeat': time_slot.repeat,
            'reminder': time_slot.reminder
        }

    #region DB CRUD methods

    @staticmethod
    def create(time_slot_attrs: EventsTimeSlotsModelInterface, app: Flask, db: SQLAlchemy) -> EventsTimeSlotModel:
        '''
        This method saves the current time slot into the database.
        If the time slot already exists in the database it will update it.
        '''
        new_time_slot: EventsTimeSlotModel = EventsTimeSlotModel()
        new_time_slot.update(time_slot_attrs)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO EventsTimeSlots(
                        time_from, 
                        time_to, 
                        location,
                        repeat,
                        reminder,
                        event_id
                    ) VALUES (?, ?, ?, ?, ?, ?);
                    """
            DBMan.execute_sql_query(app, query,(
                new_time_slot.time_form,
                new_time_slot.time_to,
                new_time_slot.location,
                new_time_slot.repeat,
                new_time_slot.reminder,
                new_time_slot.event_id
                ) 
            )
        else:
            db.session.add(new_time_slot)
            db.session.commit()
        return new_time_slot

    # @staticmethod
    # def update(time_slot: EventsTimeSlotModel, updates: EventsTimeSlotsModelInterface, app: Flask, db: SQLAlchemy) -> EventsTimeSlotModel:
    #     '''
    #     This method updates the current time slot in the database.
    #     If the time slot doesn't exist in the database it will be created.
    #     '''
    #     #TODO: implement the method
    #     pass

    # @staticmethod
    # def delete(time_slot: EventsTimeSlotModel, app: Flask, db: SQLAlchemy) -> int:
    #     '''
    #     This method deletes the current time slot from the database.
    #     If the the time slot doesn't exist in the database it will do nothing.
    #     '''

    @staticmethod
    def delete_all_by_event_id(event_id: int, app: Flask, db: SQLAlchemy):
        '''
        This method deletes all the slots that belong to a specific event which has the event_id supplied.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = '''
                    DELETE FROM EventsTimeSlots WHERE event_id = ?;
                    '''
            DBMan.execute_sql_query(app, query, (event_id,))
        else:
            for time_slot in EventsTimeSlotModelService.retrieve_slots_by_event_id(event_id, app):
                db.session.delete(time_slot)
                db.session.commit()

    @staticmethod
    def retrieve_slots_by_event_id(event_id: int, app: Flask) -> List[EventsTimeSlotModel]:
        '''
        This method searches the database for the time slots that belong to the event with the given event_id
        and returns a list of the time slots
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM EventsTimeSlots WHERE event_id = ?'
            rows = DBMan.execute_sql_query(app, query, (event_id,))

            time_slots: List[EventsTimeSlotModel] = []
            for row in rows:
                time_slot: EventsTimeSlotModel = EventsTimeSlotModel()
                time_slot.update(dict(
                    time_from = row[0],
                    time_to = row[1],
                    location = row[2],
                    repeat = row[3],
                    reminder = row[4],
                    event_id = row[5]
                ))
                time_slots.append(time_slot)

            return time_slots
        else:
            return EventsTimeSlotModel.query.filter_by(event_id = event_id).all()
