from flask import Flask
from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required

class ReminderResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        pass

    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass


class RemindersListResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        pass


class CompleteReminderResource(Resource):
    
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        pass