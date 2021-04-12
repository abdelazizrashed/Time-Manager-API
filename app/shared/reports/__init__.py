from flask import Flask
from flask_restful import Api
from .resources import ReportsListResource

def register_routes(app: Flask, api: Api):
    api.add_resource(ReportsListResource, '/reports/reports', resource_class_kwargs=dict(app = app))