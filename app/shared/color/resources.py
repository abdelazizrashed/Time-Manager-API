from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt
from ..db_man.service import db
from .models import ColorModel
from .interfaces import ColorInterface
from .services import ColorService

class ColorResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    def get(self):
        color_id: int = request.get_json()['color_id']
        if not color_id:
            return {
                'description': "The color id must be given",
                'error': "missing_info"
            }, 400
        color: ColorModel = ColorService.retrieve_by_color_id(color_id, self.app)
        if not color:
            return {
                'description': "Color not found",
                'error': "not_found"
            }, 404
        return ColorService.json(color), 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return{
                'description': "You need admin privileges",
                'error': "invalid_credentials"
            }, 401
        color_data = request.get_json()
        if not color_data['color_value']:
            return{
                'description': "The color needs a color hex value",
                'error': 'missing_info'
            }, 400
        color_attrs: ColorInterface = dict(color_value = color_data['color_value'])
        color: ColorModel = ColorService.create(color_attrs, self.app, db)
        return{
            'message': "Color created successfully",
            'color': ColorService.json(color)
        }, 201
    
    @jwt_required()
    def put(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return{
                'description': "You need admin privileges",
                'error': "invalid_credentials"
            }, 401
        color_data = request.get_json()
        if not color_data['color_id']:
            return{
                'description': "The color id must be given",
                'error': 'missing_info'
            }, 400

        if not color_data['color_value']:
            return{
                'description': "The color needs a new color hex value",
                'error': 'missing_info'
            }, 400
        color: ColorModel = ColorService.retrieve_by_color_id(color_data['color_id'], self.app)
        updates: ColorInterface = dict(color_value = color_data['color_value'])
        color = ColorService.update(color, updates, self.app, db)

        return{
            'message': "Color updated successfully.",
            'color': ColorService.json(color)
        }


    @jwt_required()
    def delete(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return{
                'description': "You need admin privileges",
                'error': "invalid_credentials"
            }, 401
        color_data = request.get_json()
        if not color_data['color_id']:
            return{
                'description': "The color id must be given",
                'error': 'missing_info'
            }, 400
        ColorService.delete(color_data['color_id'], self.app, db)
        return{
            'message': 'Color deleted successfully'
        }, 200


class ColorsListResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app

    def get(self):
        return{
            'colors': [ColorService.json(color) for color in ColorService.retrieve_all(self.app)]
        }