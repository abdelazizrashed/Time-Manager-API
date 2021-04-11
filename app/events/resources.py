import json
from flask import Flask, Request
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )

from .services import EventModelService, EventsTimeSlotModelService
from .models import EventModel, EventsTimeSlotModel
from .interfaces import EventsTimeSlotsModelInterface, EventModelInterface
from ..shared.db_man.service import db 


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
        event_data = request.get_json()

        if not event_data['event_title']:
            return {
                "description": "The event needs a title",
                "error": "missing_info"
            }, 400
        if len(event_data['time_slots']) == 0:
            return {
                "description": "You must supply at least one time slot for the event.",
                'error': "missing_info"
            }, 400
        for t_slot in event_data['time_slots']:
            if not t_slot['time_from'] or not t_slot['time_to']:
                return {
                    'description': "A time slot cannot be accepted without the beginning time and the end time of the slot",
                    'error': "missing_info"
                }, 400
            time_slot: EventsTimeSlotsModelInterface = dict(
                time_from = t_slot['time_from'], 
                time_to = t_slot['time_to'],
                location = t_slot['location'],
                repeat = t_slot['repeat'], 
                reminder = t_slot['reminder'] 
            )
            EventsTimeSlotModelService.create(time_slot, self.ap, db)
        
        event_attrs: EventModelInterface = dict(
            event_title = event_data['event_title'],
            event_description = event_data['event_description'],
            color_id = event_data['color_id'],
            parent_event_id = event_data['parent_event_id'],
            user_id = claims['user_id']
        )

        event: EventModel = EventModelService.create(event_attrs, self.app, db)
        return {
            "message": "The event created successfully",
            'event': EventModelService.json(event)
        }, 201
        

    @jwt_required()
    def put(self):
        claims = get_jwt()
        event_data = request.get_json()

        if not event_data['event_id']:
            return {
                'description': "You need to supply the event_id of the event needed to be deleted",
                'error': "missing_info"
            }, 400

        event: EventModel = EventModelService.retrieve_by_event_id(event_data['event_id'], self.app)

        if not event.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 403

        if not len(event_data['time_slots']) == 0:
            EventsTimeSlotModelService.delete_all_by_evnet_id(event.event_id, self.app, db)
            for t_slot in event_data['time_slots']:
                if not t_slot['time_from'] or not t_slot['time_to']:
                    return {
                        'description': "A time slot cannot be accepted without the beginning time and the end time of the slot",
                        'error': "missing_info"
                    }, 400
                t_slot_attr: EventsTimeSlotsModelInterface = dict(
                    time_from = t_slot['time_from'], 
                    time_to = t_slot['time_to'],
                    location = t_slot['location'],
                    repeat = t_slot['repeat'], 
                    reminder = t_slot['reminder'] 
                )
                EventsTimeSlotModelService.create(t_slot_attr, self.app, db)

                
        updates: EventModelInterface = dict(
            event_title = event_data['event_title'], 
            event_description = event_data['event_description'],
            color_id = event_data['color_id'],
            parent_event_id = event_data['parent_event_id']
        )
        
        updated_event = EventModelService.update(event, updates, self.app, db)

        return {
            "message": "Event updated successfully",
            'event': EventModelService.json(updated_event)
        }, 200

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        event_data = _event_parser.parse_args()

        if not event_data['event_id']:
            return {
                'description': "You need to supply the event_id of the event needed to be deleted",
                'error': "missing_info"
            }, 400

        event: EventModel = EventModelService.retrieve_by_event_id(event_data['event_id'], self.app)

        if not event.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 403

        try:
            EventModelService.delete(event.event_id, self.app, db)
            return {
                'message': "Event deleted successfully."
            }, 200
        except:
            return {
                'description': "An error occurred while deleting the event",
                'error': "internal_server_error"
            }, 500

class EventsListResource(Resource):
    
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        pass

class StartEventResource(Resource):

    def __init__(self, app: Flask):
        self.app = app
        
    @jwt_required()
    def post(self):
        pass

class FinishEventResource(Resource):

    def __init__(self, app: Flask):
        self.app = app
        
    @jwt_required()
    def post(self):
        pass