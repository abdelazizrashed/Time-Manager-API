from flask import Flask
from flask_restful import Api
from .resources import (
    EventResource,
    EventsResource,
    StartEventResource,
    FinishEventResource,
)


def register_routes(app: Flask, api: Api):
    api.add_resource(
        EventResource, "/events/event", resource_class_kwargs=dict(app=app)
    )
    api.add_resource(
        EventsResource, "/events/events", resource_class_kwargs=dict(app=app)
    )
    api.add_resource(
        StartEventResource, "/events/start-event", resource_class_kwargs=dict(app=app)
    )
    api.add_resource(
        FinishEventResource, "/events/finish-event", resource_class_kwargs=dict(app=app)
    )
