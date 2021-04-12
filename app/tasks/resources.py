from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_sqlalchemy import SQLAlchemy
from .models import TasksListModel, TaskModel
from .interfaces import TaskModelInterface, TasksListModelInterface
from .services import TaskModelService, TasksListModelService


class TaskResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        raise NotImplementedError
    
    @jwt_required()
    def post(self):
        raise NotImplementedError

    @jwt_required()
    def put(self):
        raise NotImplementedError

    @jwt_required()
    def delete(self):
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