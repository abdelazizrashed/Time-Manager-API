from flask import Flask
from flask_restful import Api
from .resources import ReminderResource, RemindersResource, CompleteReminderResource


def register_routes(app: Flask, api: Api):

    api.add_resource(
        ReminderResource, "/reminders/reminder", resource_class_kwargs=dict(app=app)
    )
    api.add_resource(
        RemindersResource, "/reminders/reminders", resource_class_kwargs=dict(app=app)
    )
    api.add_resource(
        CompleteReminderResource,
        "/reminders/complete-reminder",
        resource_class_kwargs=dict(app=app),
    )
