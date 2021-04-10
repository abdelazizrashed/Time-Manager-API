from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )

from .services import EventModelService, EventsTimeSlotModelService
from .models import EventModel, EventsTimeSlotsModel
from .interfaces import EventsTimeSlotsModelInterface, EventModelInterface


_event_parser = reqparse.RequestParser()
_event_parser.add_argument('event_id', type = int)
_event_parser.add_argument('event_title', type=str)
_event_parser.add_argument('event_description', type = str)
_event_parser.add_argument('is_complete', type = int)
_event_parser.add_argument('user_id', type = int)
_event_parser.add_argument('color_id', type = int)
_event_parser.add_argument('parent_event_id', type = int)
_event_parser.add_argument('time_slots', type = list)

_time_slots_parser = reqparse.RequestParser()
_time_slots_parser.add_argument('time_slot_id', type=int, location=('time_slots',))
_time_slots_parser.add_argument('time_from', type=str, location=('time_slots',))
_time_slots_parser.add_argument('time_to', type=str, location=('time_slots',))
_time_slots_parser.add_argument('location', type=str, location=('time_slots',))
_time_slots_parser.add_argument('repeat', type=str, location=('time_slots',))
_time_slots_parser.add_argument('reminder', type=str, location=('time_slots',))
_time_slots_parser.add_argument('event_id', type=int, location=('time_slots',))



class EventResource(Resource):

    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        event_args = _event_parser.parse_args()
        if not event_args['event_id']:
            return {
                "description": "No event_id found.",
                "error": "missing_info"
            }, 404
        event = EventModelService.retrieve_by_event_id(event_args['event_id'], self.app)
        if event.user_id != claims['user_id']:
            return {
                "description": "You can't access other users events.",
                "error": "invalid_credentials"
            }, 401
        return {
            "event": EventModelService.json(event)
        }, 200
        

    @jwt_required()
    def post(self):
        claims = get_jwt()
        event_args = _event_parser.parse_args()
        time_slots_args = _time_slots_parser.parse_args(req = event_args)

        event_attrs: EventModelInterface = dict(event_args)

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass


class EventsListResource(Resource):
    
    @jwt_required()
    def get(self):
        pass