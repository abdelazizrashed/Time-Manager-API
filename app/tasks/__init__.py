from flask import Flask
from flask_restful import Api

def register_routes(app: Flask, api: Api):
    from .resources import TaskResource, TasksResource, TasksListResource, StartTaskResource, FinishTaskResource

    api.add_resource(TaskResource, '/tasks/task', resource_class_kwargs=dict(app = app))
    api.add_resource(TasksResource, '/tasks/tasks', resource_class_kwargs=dict(app = app))
    api.add_resource(TasksListResource, '/tasks/tasks-list', resource_class_kwargs=dict(app = app))
    api.add_resource(StartTaskResource, '/tasks/start-task', resource_class_kwargs=dict(app = app))
    api.add_resource(FinishTaskResource, '/tasks/finish-task', resource_class_kwargs=dict(app = app))