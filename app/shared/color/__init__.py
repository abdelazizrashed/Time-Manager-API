from flask import Flask
from flask_restful import Api

def register_routes(app: Flask, api: Api):
    from .resources import ColorResource, ColorsListResource

    api.add_resource(ColorResource, '/colors/color', resource_class_kwargs=dict(app = app))
    api.add_resource(ColorsListResource, '/colors/colors', resource_class_kwargs=dict(app = app))