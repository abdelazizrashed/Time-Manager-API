from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import get_jwt, jwt_required
from .models import ReminderModel, RemindersTimeSlotModel
from .interfaces import ReminderModelInterface, RemindersTimeSlotModelInterface
from .services import ReminderModelService, RemindersTimeSlotModelService
from ..shared.db_man.service import db
from ..shared.reports.services import ReportService


class ReminderResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        reminder_data = request.get_json()
        if not reminder_data['reminder_id']:
            return {
                "description": "No reminder_id found.",
                "error": "missing_info"
            }, 404
        
        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(reminder_data['reminder_id'], self.app)
        if reminder.user_id != claims['user_id']:
            return {
                "description": "You can't access other users data.",
                "error": "invalid_credentials"
            }, 401
        return {
            "reminder": ReminderModelService.json(reminder)
        }, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        if not reminder_data['reminder_title']:
            return {
                "description": "The reminder needs a title",
                "error": "missing_info"
            }, 400
        if len(reminder_data['time_slots']) == 0:
            return {
                "description": "You must supply at least one time slot for the reminder.",
                'error': "missing_info"
            }, 400
        for t_slot in reminder_data['time_slots']:
            if not t_slot['time_from'] or not t_slot['time_to']:
                return {
                    'description': "A time slot cannot be accepted without the beginning time and the end time of the slot",
                    'error': "missing_info"
                }, 400
            time_slot: RemindersTimeSlotModelInterface = dict(
                time = t_slot['time_from'],
                repeat = t_slot['repeat'], 
                reminder = t_slot['reminder'],
                reminder_id = reminder_data['reminder_id']
            )
            RemindersTimeSlotModelService.create(time_slot, self.ap, db)
        
        reminder_attrs: ReminderModelInterface = dict(
            reminder_title = reminder_data['reminder_title'],
            reminder_description = reminder_data['reminder_description'],
            color_id = reminder_data['color_id'],
            parent_event_id = reminder_data['parent_event_id'],
            user_id = claims['user_id']
        )

        reminder: ReminderModel = ReminderModelService.create(reminder_attrs, self.app, db)
        return {
            "message": "The reminder created successfully",
            'reminder': ReminderModelService.json(reminder, app)
        }, 201

    @jwt_required()
    def put(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        if not reminder_data['reminder_id']:
            return {
                'description': "You need to supply the reminder_id of the reminder needed to be updated",
                'error': "missing_info"
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(reminder_data['reminder_id'], self.app)

        if not reminder.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 401

        if not len(reminder_data['time_slots']) == 0:
            RemindersTimeSlotModelService.delete_all_by_reminder_id(reminder.reminder_id, self.app, db)
            for t_slot in reminder_data['time_slots']:
                if not t_slot['time_from'] or not t_slot['time_to']:
                    return {
                        'description': "A time slot cannot be accepted without the beginning time and the end time of the slot",
                        'error': "missing_info"
                    }, 400
                t_slot_attr: RemindersTimeSlotsModelInterface = dict(
                    time = t_slot['time_from'], 
                    repeat = t_slot['repeat'], 
                    reminder = t_slot['reminder'],
                    reminder_id = reminder_data['reminder_id']
                )
                RemindersTimeSlotModelService.create(t_slot_attr, self.app, db)

                
        updates: ReminderModelInterface = dict(
            reminder_title = reminder_data['reminder_title'], 
            reminder_description = reminder_data['reminder_description'],
            color_id = reminder_data['color_id'],
            parent_event_id = reminder_data['parent_event_id']
        )
        
        updated_reminder = ReminderModelService.update(reminder, updates, self.app, db)

        return {
            "message": "reminder updated successfully",
            'reminder': ReminderModelService.json(updated_reminder)
        }, 200

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        if not reminder_data['reminder_id']:
            return {
                'description': "You need to supply the reminder_id of the reminder needed to be deleted",
                'error': "missing_info"
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(reminder_data['reminder_id'], self.app)

        if not reminder.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 401
        #TODO: delete the reports of the reminder.
        try:
            ReminderModelService.delete(reminder.reminder_id, self.app, db)
            return {
                'message': "reminder deleted successfully."
            }, 200
        except:
            return {
                'description': "An error occurred while deleting the reminder",
                'error': "internal_server_error"
            }, 500


class RemindersListResource(Resource):

    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        return {
            "reminders": [ReminderModelService.json(reminder) for reminder in ReminderModelService.retrieve_reminders_by_user_id(claims['user_id'], self.app)]
        }, 200


class CompleteReminderResource(Resource):
    
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        if not reminder_data['reminder_id']:
            return {
                'description': "You need to supply the reminder_id of the reminder needed to be registered as finished",
                'error': "missing_info"
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(reminder_data['reminder_id'], self.app)

        if not reminder:
            return {
                "description": "Reminder couldn't be found.",
                'error': "not_found"
            }, 404

        if not reminder.user_id == claims['user_id']:
            return {
                "description": "Can't access other users data",
                'error': 'invalid_credentials'
            }, 401

        try:
            report: ReportModel = ReportService.finish_a_reminder(reminder.reminder_id, reminder_data['time'], self.app, db)
            return{
                "message": "Reminder registered as complete successfully",
                "report": ReportService.json(report)
            }, 200
        except:
            return{
                'description': "Failure will registering the reminder",
                'error': "internal_server_error"
            }, 500