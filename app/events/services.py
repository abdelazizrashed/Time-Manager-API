from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from ..shared.db_man.service import DBMan
from .models import EventModel, EventsTimeSlotModel
from .interfaces import EventModelInterface, EventsTimeSlotModelInterface


class EventModelService:

    @staticmethod
    def json(event: EventModel):
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
            'parent_event_id': event.parent_event_id
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


    @staticmethod
    def update(event: EventModel, updates: EventModelInterface) -> EventModel:
        '''
        This method update the current event in the database.
        If the event already exists it will save it to the database.
        '''
        if not self.find_by_event_id(self.event_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE
                        SET event_title = ?, event_description = ?, is_completed = ?, user_id = ?, color_id = ?, parent_event_id = ?
                        WHERE event_id = ?;
                        """
                curser.execute(query, (
                    self.event_title, 
                    self.event_description,
                    self.is_completed,
                    self.user_id,
                    self.color_id,
                    self.parent_event_id,
                    self.event_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()


    @staticmethod
    def delete(event_id: int) -> int:
        '''
        This method will delete the current event from the database only if it exists.
        '''
        if self.find_by_event_id(self.event_id):
            #TODO: delete all tasks that have this event as its parent

            events = self.find_events_by_parent_id(self.event_id)
            for event in events:
                event.delete_from_db()
            
            time_slots = EventsTimeSlotModel.find_slots_by_event_id(self.event_id)
            for time_slot in time_slots:
                time_slot.delete_from_db()

            if app.app.config['DEBUG']:
                connection = sqlite3.connect(db_url)
                curser = connection.cursor()

                query = 'DELETE FROM Events WHERE event_id = ?;'
                curser.execute(query, (self.event_id,))

                connection.commit()
                connection.close()
            else:
                db.session.delete(self)
                db.session.commit()

    
    @staticmethod
    def retrieve_by_event_id(event_id: int) -> EventModel:
        '''
        This method searchs the database for an event with the given event id.
        If the event does not exist it will return None.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Events WHERE event_id = ?;'

            result = curser.execute(query, (event_id,))
            row = result.fetchone()
            if row:
                event = cls(*row)
            else:
                event = None

            connection.close()
            return event

        else:
            return cls.query.filter_by(event_id = event_id).first()

    
    @staticmethod
    def retrieve_events_by_parent_id(parent_event_id: int) -> List[EventModel]:
        '''
        This method finds events by its parent event id and return a list of event that match.
        If nothing found it will return and empty list.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.connect(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Events WHERE parent_event_id = ?'
            result = curser.execute(query, (parent_event_id,))

            events = []
            for row in result:
                event = cls(*row)
                events.append(event)
            
            connection.close()
            return events
        else:
            return cls.query.filter_by(parent_event_id = parent_event_id).all()
    #endregion

class EventsTimeSlotModelService:
    pass