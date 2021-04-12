from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_sqlalchemy import SQLAlchemy
from ..shared.db_man.service import db
from .models import TasksListModel, TaskModel
from .interfaces import TaskModelInterface, TasksListModelInterface
from .services import TaskModelService, TasksListModelService


class TaskResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        task_data = request.get_json()
        if not task_data['task_id']:
            return {
                "description": "No task id found.",
                "error": "missing_info"
            }, 400
        task = TaskModelService.retrieve_by_task_id(task_data['task_id'], self.app)
        if task.user_id != claims['user_id']:
            return {
                "description": "You can't access other users events.",
                "error": "invalid_credentials"
            }, 401
        return TaskModelService.json(task, self.app), 200
    
    @jwt_required()
    def post(self):
        claims = get_jwt()
        task_data = request.get_json()

        if not task_data['task_title']:
            return {
                "description": "The task needs a title",
                "error": "missing_info"
            }, 400

        if not task_data['time_from'] or not task_data['time_to']:
            return {
                "description": "The task needs a start time and a finish time",
                "error": "missing_info"
            }, 400

        if not task_data['list_id']:
            return {
                "description": "The task needs to belong to a list",
                "error": "missing_info"
            }, 400

        if not task_data['color_id']:
            return {
                "description": "The task must have an identifying color",
                "error": "missing_info"
            }, 400
        

        task_attrs: TaskModelInterface = dict(
            task_title = task_data['task_title'],
            task_description = task_data['task_description'],
            time_from = task_data['time_from'],
            time_to = task_data['time_to'],
            time_started = task_data['time_started'],
            time_finished = task_data['time_finished'],
            is_complete = task_data['is_complete'],
            reminder = task_data['reminder'],
            repeat = task_data['repeat'],
            list_id = task_data['list_id'],
            color_id = task_data['color_id'],
            user_id = claims['user_id'],
            parent_event_id = task_data['parent_event_id'],
            parent_task_id = task_data['parent_task_id']
        )

        task: EventModel = TaskModelService.create(task_attrs, self.app, db)
        return {
            "message": "The task created successfully",
            'task': TaskModelService.json(task)
        }, 201

    @jwt_required()
    def put(self):
        claims = get_jwt()
        task_data = request.get_json()

        if not task_data['task_id']:
            return {
                'description': "You need to supply the task_id of the task needed to be modified",
                'error': "missing_info"
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_task_id(task_data['task_id'], self.app)

        if not task.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 401
                
        updates: TaskModelInterface = dict(
            task_title = task_data['task_title'],
            task_description = task_data['task_description'],
            time_from = task_data['time_from'],
            time_to = task_data['time_to'],
            time_started = task_data['time_started'],
            time_finished = task_data['time_finished'],
            is_complete = task_data['is_complete'],
            reminder = task_data['reminder'],
            repeat = task_data['repeat'],
            list_id = task_data['list_id'],
            color_id = task_data['color_id'],
            user_id = claims['user_id'],
            parent_event_id = task_data['parent_event_id'],
            parent_task_id = task_data['parent_task_id']
        )
        
        return {
            "message": "Task updated successfully",
            'task': TaskModelService.json(TaskModelService.update(task, updates, self.app, db))
        }, 200

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        data = request.get_json()

        if not data['task_id']:
            return {
                'description': "You need to supply the task_id of the task needed to be deleted",
                'error': "missing_info"
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_event_id(data['taskid'], self.app)

        if not task.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 401
        #TODO: delete the reports of the event.
        try:
            TaskModelService.delete(task.task_id, self.app, db)
            return {
                'message': "Task deleted successfully."
            }, 200
        except:
            return {
                'description': "An error occurred while deleting the task",
                'error': "internal_server_error"
            }, 500


class TasksResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        raise NotImplementedError


class TasksListResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        raise NotImplementedError


class StartTaskResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        raise NotImplementedError


class FinishTaskResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        raise NotImplementedError