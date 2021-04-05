import sqlite3
import app

from db_man import db, db_url
from models.events_time_slot_model import EventsTimeSlotModel




class EventModel(db.Model):

    __tablename__ = 'Events'

    #region SQLAlchemy table columns

    event_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    event_title = db.Column(
        db.String(50),
        nullable = False
    )

    event_description = db.Column(
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

    def __init__(
        self, 
        event_id,
        event_title,
        event_description,
        is_completed,
        user_id,
        color_id,
        parent_event_id
        ):
        self.event_id = event_id
        self.event_title = event_title
        self.event_description = event_description
        self.is_completed = is_completed
        self.user_id = user_id
        self.color_id = color_id
        self.parent_event_id = parent_event_id

    def json(self):
        '''
        This method return the object in JSON format
        '''
        #TODO: change it so that it return the json of the time slots as well as the json of the color
        return {
            'event_id': self.event_id,
            'event_title': self.event_title,
            'event_description': self.event_description,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'color_id': self.color_id,
            'parent_event_id': self.parent_event_id
        }
    
    #region DB methods
    def save_to_db(self):
        '''
        This method saves the current event to the database.
        If the event already exists it will just update it.
        '''
        if self.find_by_event_id(self.event_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO Events VALUES (NULL, ?, ?, ?, ?, ?, ?);
                        """
                curser.execute(query, (
                    self.event_title, 
                    self.event_description,
                    self.is_completed,
                    self.user_id,
                    self.color_id,
                    self.parent_event_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    def update_in_db(self):
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

    def delete_from_db(self):
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

    @classmethod
    def find_by_event_id(cls, event_id):
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

    @classmethod
    def find_events_by_parent_id(cls, parent_event_id):
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