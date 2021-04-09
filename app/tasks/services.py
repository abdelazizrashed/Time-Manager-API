from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .interfaces import TaskModelInterface, TasksListModelInterface
from .models import TaskModel, TasksListModel

class TaskModelService:

    @staticmethod
    def json(task: TaskModel):
        '''
        This method returns the current task in JSON format
        '''
        #TODO: modify it so that it returns the children as well
        return{
            'task_id': task.task_id,
            'task_title': task.task_title,
            'task_description': task.task_description,
            'time_from': task.time_form,
            'time_to': task.time_to,
            'time_started': task.time_started,
            'is_completed': task.is_completed,
            'repeat': task.repeat,
            'reminder': task.reminder,
            'list_id': task.list_id,
            'color_id': task.color_id,
            'user_id': task.user_id,
            'parent_event_id': task.parent_event_id,
            'parent_task_id': task.parent_task_id
        }

    #region DB  CRUD methods

    @staticmethod
    def create(taks_attrs: TaskModelInterface, app: Flask, db: SQLAlchemy) -> TaskModel:
        '''
        This method saves the current task to the database.
        If the task already exists it will update it.
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def update(task: TaskModel, updates: TaskModelInterface, app: Flask, db: SQLAlchemy) -> TaskModel:
        '''
        This method updates the current task in the DB.
        If the task does not exit in the DB it will save it.
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def delete(task_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method deletes the currnet task from the database.
        If the task doesn't exist it will do nothing
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def retrieve_by_task_id(task_id: int, app: Flask) -> TaskModel:
        '''
        This method searchs the DB for a task with the given task_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def retrieve_tasks_by_parent_task_id(parent_task_id: int, app: Flask) -> List[TaskModel]:
        '''
        This methods searchs the DB for tasks that have the task with the given id as a parent and returns them in a list.
        If nothing could be found, it will return an empty list
        '''
        #TODO: implement this method
        pass

    @staticmethod
    def retrieve_tasks_by_parent_event_id(parent_event_id: int, app: Flask) -> List[TaskModel]:
        '''
        This method searchs the DB for the tasks that have the event with the given id as a parent and return them in the form of a list.
        If nothing could be found it will return an empty list.
        '''
        #TODO: implement this method
        pass

    #endregion


class TasksListModelService:

    @staticmethod
    def json(list: TasksListModelInterface):
        '''
        This method return the object in JSON format
        '''
        #TODO: a second thougt
        return {
            'list_id': list.list_id,
            'list_title': list.list_title
        }
    #region DB methods

    @staticmethod
    def create(list_attrs: TasksListModelInterface, app: Flask, db: SQLAlchemy) -> TasksListModel:
        '''
        This method saves the current TasksList to the database.
        If the Tasks List already exists it will just update it.
        '''
        if self.find_by_list_id(self.list_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO TasksLists VALUES (NULL, ?);
                        """
                curser.execute(query, (
                    self.list_title,
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    @staticmethod
    def update(list: TasksListModel, updates: TasksListModelInterface, app: Flask, db: SQLAlchemy) -> TasksListModel:
        '''
        This method will update the current TasksList in the database with its current values.
        If the TasksList does not exist in the database it will save it.
        '''
        if not self.find_by_list_id(self.list_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE TasksLists
                        SET list_title = ?
                        WHERE list_id = ?;
                        """
                curser.execute(query, (
                    self.list_title,
                    self.list_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()

    @staticmethod
    def delete(list_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method will delete the TasksList and its tasks from the database only if it exists.
        '''
        if find_by_list_id(self.color_id):
            if app.app.config['DEBUG']:
                #TODO: delete the tasks the belong to this tasks list
                connection = sqlite3.connect(db_url)
                curser = connection.cursor()

                query = 'DELETE FROM TasksLists WHERE list_id = ?;'
                curser.execute(query, (self.list_id,))

                connection.commit()
                connection.close()
            else:
                 #TODO: delete the tasks the belong to this tasks list
                db.session.delete(self)
                db.session.commit()

    @staticmethod
    def retrieve_by_list_id(list_id: int, app: Flask) -> TasksListModel:
        '''
        This method searchs the database for a list with the given list id.
        If the list does not exist it will return None.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM TasksLIsts WHERE list_id = ?;'

            result = curser.execute(query, (list_id,))
            row = result.fetchone()
            if row:
                new_list = cls(*row)
            else:
                new_list = None

            connection.close()
            return new_list

        else:
            return cls.query.filter_by(list_id = list_id).first()

    #endregion