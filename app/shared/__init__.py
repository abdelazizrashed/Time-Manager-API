from flask import Flask
from flask_restful import Api

def register_routes(app: Flask, api: Api):
    from .color import register_routes as attach_colors
    from .reports import register_routes as attach_reports
    
    attach_colors(app, api)
    attach_reports(app, api)