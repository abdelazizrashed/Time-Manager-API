from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from ..shared.db_man.service import DBMan
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
            'time_finished': task.time_finished,
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
    def create(task_attrs: TaskModelInterface, app: Flask, db: SQLAlchemy) -> TaskModel:
        '''
        This method saves the current task to the database.
        If the task already exists it will update it.
        '''
        new_task: TaskModel = TaskModel()
        new_task.update(task_attrs)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO Tasks(
                        task_title,
                        task_description,
                        time_from,
                        time_to,
                        time_started,
                        time_finished,
                        is_complete,
                        repeat,
                        reminder,
                        list_id,
                        color_id,
                        user_id,
                        parent_event_id,
                        parent_task_id
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """
            rows_n_rowid = list(DBMan.execute_sql_query(app, query,(
                    new_task.task_title,
                    new_task.task_description,
                    new_task.time_from ,
                    new_task.time_to,
                    new_task.time_started,
                    new_task.time_finished,
                    new_task.is_complete,
                    new_task.repeat,
                    new_task.reminder,
                    new_task.list_id,
                    new_task.color_id,
                    new_task.user_id,
                    new_task.parent_event_id,
                    new_task.parent_task_id
                ) 
            ))
            return new_task.update(dict(task_id = rows_n_rowid[0]))
        else:
            db.session.add(new_task)
            db.session.commit()
            return new_task

    @staticmethod
    def update(task: TaskModel, updates: TaskModelInterface, app: Flask, db: SQLAlchemy) -> TaskModel:
        '''
        This method updates the current task in the DB.
        If the task does not exit in the DB it will save it.
        '''
        if not TaskModelService.retrieve_by_event_id(task.task_id):
            return TaskModelService.create(updates, app, db)
        new_task = task.update(updates)
        if app.config['DEBUG']:
            query = """
                    UPDATE Events
                    SET task_title = ?, 
                    task_description = ?,
                    time_from = ?,
                    time_to = ?,
                    time_started = ?,
                    time_finished = ?, 
                    is_completed = ?,
                    repeat = ?,
                    reminder = ?,
                    list_id = ?, 
                    color_id = ?, 
                    user_id = ?, 
                    parent_event_id = ?,
                    parent_task_id = ?,
                    WHERE task_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (
                    new_task.task_title,
                    new_task.task_description,
                    new_task.time_from ,
                    new_task.time_to,
                    new_task.time_started,
                    new_task.time_finished,
                    new_task.is_complete,
                    new_task.repeat,
                    new_task.reminder,
                    new_task.list_id,
                    new_task.color_id,
                    new_task.user_id,
                    new_task.parent_event_id,
                    new_task.parent_task_id,
                    new_task.task_id
                )
            )
        else:
            db.session.commit()
        return new_task

    @staticmethod
    def delete(task_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method deletes the current task from the database.
        If the task doesn't exist it will do nothing
        '''
        task: TaskModel = TaskModelService.retrieve_by_task_id(task_id)
        if task:

            tasks: TaskModel = TaskModelService.retrieve_tasks_by_parent_task_id(task_id, app)
            for t in tasks:
                TaskModelService.delete(t.task_id, app, db)
                

            if app.config['DEBUG'] or app.config['TESTING']:
                
                query = 'DELETE FROM Tasks WHERE task_id = ?;'
                DBMan.execute_sql_query(app, query, (task_id, ))
                
            else:
                db.session.delete(task)
                db.session.commit()
            return task_id
        return None

    @staticmethod
    def retrieve_by_task_id(task_id: int, app: Flask) -> TaskModel:
        '''
        This method searches the DB for a task with the given task_id.
        If nothing could be found it will return None.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Tasks WHERE task_id = ?;'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (task_id,)))
            task: TaskModel = TaskModel()
            for row in rows_n_rowid[1]:
                return task.update(dict(
                    task_id = row[0],
                    task_title = row[1],
                    task_description = row[2],
                    time_from = row[3],
                    time_to = row[4],
                    time_started = row[5],
                    time_finished = row[6],
                    is_complete = row[7],
                    repeat = row[8],
                    reminder = row[9],
                    list_id = row[10],
                    color_id = row[11],
                    user_id = row[12],
                    parent_event_id = row[13],
                    parent_task_id = row[14]
                ))
            return None

        else:
            return TaskModel.query.filter_by(task_id = task_id).first()

    @staticmethod
    def retrieve_tasks_by_parent_task_id(parent_task_id: int, app: Flask) -> List[TaskModel]:
        '''
        This methods searches the DB for tasks that have the task with the given id as a parent and returns them in a list.
        If nothing could be found, it will return an empty list
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Tasks WHERE parent_task_id = ?'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (parent_task_id,)))

            tasks: List[TaskModel] = []
            for row in rows_n_rowid[1]:
                task: TaskModel = TaskModel()
                tasks.append(task.update(dict(
                    task_id = row[0],
                    task_title = row[1],
                    task_description = row[2],
                    time_from = row[3],
                    time_to = row[4],
                    time_started = row[5],
                    time_finished = row[6],
                    is_complete = row[7],
                    repeat = row[8],
                    reminder = row[9],
                    list_id = row[10],
                    color_id = row[11],
                    user_id = row[12],
                    parent_event_id = row[13],
                    parent_task_id = row[14]
                )))

            return tasks
        else:
            return TaskModel.query.filter_by(parent_task_id = parent_task_id).all()

    @staticmethod
    def retrieve_tasks_by_parent_event_id(parent_event_id: int, app: Flask) -> List[TaskModel]:
        '''
        This method searches the DB for the tasks that have the event with the given id as a parent and return them in the form of a list.
        If nothing could be found it will return an empty list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Tasks WHERE parent_event_id = ?'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (parent_event_id,)))

            tasks: List[TaskModel] = []
            for row in rows_n_rowid[1]:
                task: TaskModel = TaskModel()
                tasks.append(task.update(dict(
                    task_id = row[0],
                    task_title = row[1],
                    task_description = row[2],
                    time_from = row[3],
                    time_to = row[4],
                    time_started = row[5],
                    time_finished = row[6],
                    is_complete = row[7],
                    repeat = row[8],
                    reminder = row[9],
                    list_id = row[10],
                    color_id = row[11],
                    user_id = row[12],
                    parent_event_id = row[13],
                    parent_task_id = row[14]
                )))

            return tasks
        else:
            return TaskModel.query.filter_by(parent_event_id = parent_event_id).all()


    @staticmethod
    def retrieve_tasks_by_user_id(user_id: int, app: Flask) -> List[TaskModel]:
        '''
        This method searches the DB for the tasks that have the event with the given id as a parent and return them in the form of a list.
        If nothing could be found it will return an empty list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Tasks WHERE user_id = ?'
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (user_id,)))

            tasks: List[TaskModel] = []
            for row in rows_n_rowid[1]:
                task: TaskModel = TaskModel()
                tasks.append(task.update(dict(
                    task_id = row[0],
                    task_title = row[1],
                    task_description = row[2],
                    time_from = row[3],
                    time_to = row[4],
                    time_started = row[5],
                    time_finished = row[6],
                    is_complete = row[7],
                    repeat = row[8],
                    reminder = row[9],
                    list_id = row[10],
                    color_id = row[11],
                    user_id = row[12],
                    parent_event_id = row[13],
                    parent_task_id = row[14]
                )))

            return tasks
        else:
            return TaskModel.query.filter_by(user_id = user_id).all()
            
    #endregion


class TasksListModelService:

    @staticmethod
    def json(list: TasksListModelInterface):
        '''
        This method return the object in JSON format
        '''
        #TODO: a second thought
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
        new_list: TasksListModel = TasksListModel()
        new_list.update(list_attrs)
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO TasksLists VALUES (NULL, ?);
                    """
            DBMan.execute_sql_query(app, query, (new_list.list_title))
        else:
            db.session.add(new_list)
            db.session.commit()

    @staticmethod
    def update(_list: TasksListModel, updates: TasksListModelInterface, app: Flask, db: SQLAlchemy) -> TasksListModel:
        '''
        This method will update the current TasksList in the database with its current values.
        If the TasksList does not exist in the database it will save it.
        '''
        _list.update(updates)
        if not TasksListModelService.retrieve_by_list_id(_list.list_id):
            return TasksListModelService.create(updates, app, db)

        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    UPDATE TasksLists
                    SET list_title = ?
                    WHERE list_id = ?;
                    """

            DBMan.execute_sql_query(app, query, (
                _list.list_title,
                _list.list_id
                )
            )
        else:
            db.session.commit()

    @staticmethod
    def delete(list_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method will delete the TasksList and its tasks from the database only if it exists.
        '''
        _list: TasksListModel = TasksListModelService.retrieve_by_list_id(list_id, app)
        if not _list:
            return None

        tasks: List[TaskModel] = TaskModelService.retrieve_tasks_by_parent_task_id(list_id, app)
        for task in tasks:
            TaskModelService.delete(task.task_id, app, db)

        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'DELETE FROM TasksLists WHERE list_id = ?;'
            
            DBMan.execute_sql_query(app, query, (_list.list_id,))

        else:
            db.session.delete(_list)
            db.session.commit()
        return list_id

    @staticmethod
    def retrieve_by_list_id(list_id: int, app: Flask) -> TasksListModel:
        '''
        This method searches the database for a list with the given list id.
        If the list does not exist it will return None.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            new_list: TasksListModel = TasksListModel()
            query = 'SELECT * FROM TasksLists WHERE list_id = ?;'
            
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (list_id, )))
            for row in rows_n_rowid[1]:
                return new_list.update(dict(
                    list_id = row[0],
                    list_title = row[1]
                ))

        else:
            return TasksListModel.query.filter_by(list_id = list_id).first()

    @staticmethod
    def retrieve_lists_by_user_id(user_id: int, app: Flask) -> List[TasksListModel]:
        '''
        This method searches the database for a list with the given list id.
        If the list does not exist it will return None.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            
            lists: List[TasksListModel] = []

            query = 'SELECT * FROM TasksLists WHERE user_id = ?;'
            
            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (user_id, )))
            for row in rows_n_rowid[1]:
                new_list: TasksListModel = TasksListModel()
                lists.append( new_list.update(dict(
                    list_id = row[0],
                    list_title = row[1]
                )))
            return lists

        else:
            return TasksListModel.query.filter_by(user_id = user_id).all()

    #endregion