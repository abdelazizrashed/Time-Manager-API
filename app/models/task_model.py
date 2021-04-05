from db_man import db, db_url
import sqlite3
import app



class TaskModel(db.Model):
    __tablename__ = 'Tasks'

    #region SQLAlchemy table columns

    task_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    task_title = db.Column(
        db.String(50),
        nullable = False
    )

    task_description = db.Column(
        db.String(250),
        nullable = True,
        default = None
    )

    time_form = db.Column(
        db.String(100),
        nullable = False
    )

    time_to = db.Column(
        db.String(100),
        nullable = False
    )

    time_started = db.Column(
        db.String(100),
        nullable = False
    )

    time_finished = db.Column(
        db.String(100),
        nullable = False
    )

    is_completed = db.Column(
        db.Boolean,
        nullable = True,
        default = 0
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

    list_id = db.Column(
        db.Integer,
        db.ForeignKey('Lists.list_id'),
        nullable = False
    )

    color_id = db.Column(
        db.Integer,
        db.ForeignKey('Colors.color_id'),
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('Users.user_id'),
        nullable = False
    )

    parent_event_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = True,
        default = None
    )

    parent_task_id = db.Column(
        db.Integer,
        db.ForeignKey('Events.event_id'),
        nullable = True,
        default = None
    )

    #endregion

    def __init__(
        self,
        task_id,
        task_title,
        task_description,
        time_from,
        time_to,
        time_started,
        time_finished,
        is_completed,
        repeat,
        reminder,
        list_id,
        color_id,
        user_id,
        parent_event_id,
        parent_task_id
        ):
        self.task_id = task_id
        self.task_title =task_title
        self.task_description = task_description
        self.time_form = time_from
        self.time_to = time_to
        self.time_started = time_started
        self.time_finished = time_finished
        self.is_completed = is_completed
        self.repeat = repeat
        self.reminder = reminder
        self.list_id =list_id
        self.color_id = color_id
        self.user_id = user_id
        self.parent_event_id = parent_event_id
        self.parent_task_id = parent_task_id

    def json(self):
        '''
        This method returns the current task in JSON format
        '''
        #TODO: modify it so that it returns the children as well
        return{
            'task_id': self.task_id,
            'task_title': self.task_title,
            'task_description': self.task_description,
            'time_from': self.time_form,
            'time_to': self.time_to,
            'time_started': self.time_started,
            'is_completed': self.is_completed,
            'repeat': self.repeat,
            'reminder': self.reminder,
            'list_id': self.list_id,
            'color_id': self.color_id,
            'user_id': self.user_id,
            'parent_event_id': self.parent_event_id,
            'parent_task_id': self.parent_task_id
        }

    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current task to the database.
        If the task already exists it will update it.
        '''
        #TODO: implement this method
        pass

    def update_in_db(self):
        '''
        This method updates the current task in the DB.
        If the task does not exit in the DB it will save it.
        '''
        #TODO: implement this method
        pass

    def delete_from_db(self):
        '''
        This method deletes the currnet task from the database.
        If the task doesn't exist it will do nothing
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_by_task_id(self, task_id):
        '''
        This method searchs the DB for a task with the given task_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_tasks_by_parent_task_id(self, parent_task_id):
        '''
        This methods searchs the DB for tasks that have the task with the given id as a parent and returns them in a list.
        If nothing could be found, it will return an empty list
        '''
        #TODO: implement this method
        pass

    @classmethod 
    def find_tasks_by_parent_event_id(self, parent_event_id):
        '''
        This method searchs the DB for the tasks that have the event with the given id as a parent and return them in the form of a list.
        If nothing could be found it will return an empty list.
        '''
        #TODO: implement this method
        pass

    #endregion