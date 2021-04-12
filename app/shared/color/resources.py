from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt

class ColorResource(Resource):

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


class ColorsListResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        raise NotImplementedError