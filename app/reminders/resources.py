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
        if not reminder_data["reminder_id"]:
            return {
                "description": "No reminder_id found.",
                "error": "missing_info",
            }, 404

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(
            reminder_data["reminder_id"], self.app
        )
        if reminder.user_id != claims.get("user_id"):
            return {
                "description": "You can't access other users data.",
                "error": "invalid_credentials",
            }, 401
        return {"reminder": ReminderModelService.json(reminder, self.app)}, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        return Helper.create_reminder(reminder_data, claims, self.app)

    @jwt_required()
    def put(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        return Helper.update_reminder(reminder_data, claims, self.app)

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        return Helper.delete_reminder(reminder_data, claims, self.app)


class RemindersResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        return {
            "reminders": [
                ReminderModelService.json(reminder, self.app)
                for reminder in ReminderModelService.retrieve_reminders_by_user_id(
                    claims.get("user_id"), self.app
                )
            ]
        }, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        data = request.get_json()
        return {
            "messages": [
                Helper.create_reminder(reminder_data, claims, self.app)
                for reminder_data in data["reminders"]
            ]
        }

    @jwt_required()
    def put(self):
        claims = get_jwt()
        data = request.get_json()
        return {
            "messages": [
                Helper.update_reminder(reminder_data, claims, self.app)
                for reminder_data in data["reminders"]
            ]
        }

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        data = request.get_json()
        return {
            "messages": [
                Helper.delete_reminder(reminder_data, claims, self.app)
                for reminder_data in data["reminders"]
            ]
        }


class CompleteReminderResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        claims = get_jwt()
        reminder_data = request.get_json()

        if not reminder_data.get("reminder_id"):
            return {
                "description": "You need to supply the reminder_id of the reminder needed to be registered as finished",
                "error": "missing_info",
            }, 400

        if not reminder_data.get("time"):
            return {
                "description": "You need to supply the time of completion",
                "error": "missing_info",
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(
            reminder_data["reminder_id"], self.app
        )

        if not reminder:
            return {
                "description": "Reminder couldn't be found.",
                "error": "not_found",
            }, 404

        if not reminder.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401

        report: ReportModel = ReportService.finish_a_reminder(
            reminder.reminder_id, reminder.user_id, reminder_data["time"], self.app, db
        )
        return {
            "message": "Reminder registered as complete successfully",
            "report": ReportService.json(report),
        }, 200
        # try:
        # except:
        #     return {
        #         "description": "Failure will registering the reminder",
        #         "error": "internal_server_error",
        #     }, 500


class Helper:
    @staticmethod
    def create_reminder(reminder_data: dict, claims: dict, app: Flask):

        if not reminder_data["reminder_title"]:
            return {
                "description": "The reminder needs a title",
                "error": "missing_info",
            }, 400
        if len(reminder_data["time_slots"]) == 0:
            return {
                "description": "You must supply at least one time slot for the reminder.",
                "error": "missing_info",
            }, 400

        for t_slot in reminder_data["time_slots"]:
            if not t_slot["time"]:
                return {
                    "description": "A time slot cannot be accepted without the beginning time and the end time of the slot",
                    "error": "missing_info",
                }, 400

        reminder: ReminderModel = ReminderModelService.create(
            dict(
                reminder_title=reminder_data["reminder_title"],
                reminder_description=reminder_data["reminder_description"],
                color_id=reminder_data["color_id"],
                parent_event_id=reminder_data["parent_event_id"],
                user_id=claims.get("user_id"),
            ),
            app,
            db,
        )
        for t_slot in reminder_data["time_slots"]:
            RemindersTimeSlotModelService.create(
                dict(
                    time=t_slot["time"],
                    repeat=t_slot["repeat"],
                    reminder=t_slot["reminder"],
                    reminder_id=reminder.reminder_id,
                ),
                app,
                db,
            )
        return {
            "message": "The reminder created successfully",
            "reminder": ReminderModelService.json(reminder, app),
        }, 201

    @staticmethod
    def update_reminder(reminder_data: dict, claims: dict, app: Flask):

        if not reminder_data.get("reminder_id"):
            return {
                "description": "You need to supply the reminder_id of the reminder needed to be updated",
                "error": "missing_info",
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(
            reminder_data["reminder_id"], app
        )

        if not reminder.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401

        if not len(reminder_data["time_slots"]) == 0:
            RemindersTimeSlotModelService.delete_all_by_reminder_id(
                reminder.reminder_id, app, db
            )
            for t_slot in reminder_data["time_slots"]:
                if not t_slot["time"]:
                    return {
                        "description": "A time slot cannot be accepted without the beginning time and the end time of the slot",
                        "error": "missing_info",
                    }, 400
                t_slot_attr: RemindersTimeSlotsModelInterface = dict(
                    time=t_slot["time"],
                    repeat=t_slot["repeat"],
                    reminder=t_slot["reminder"],
                    reminder_id=reminder_data["reminder_id"],
                )
                RemindersTimeSlotModelService.create(t_slot_attr, app, db)

        updates: ReminderModelInterface = dict(
            reminder_title=reminder_data["reminder_title"],
            reminder_description=reminder_data["reminder_description"],
            color_id=reminder_data["color_id"],
            parent_event_id=reminder_data["parent_event_id"],
        )

        updated_reminder = ReminderModelService.update(reminder, updates, app, db)

        return {
            "message": "reminder updated successfully",
            "reminder": ReminderModelService.json(updated_reminder, app),
        }, 200

    @staticmethod
    def delete_reminder(reminder_data: dict, claims: dict, app: Flask):

        if not reminder_data["reminder_id"]:
            return {
                "description": "You need to supply the reminder_id of the reminder needed to be deleted",
                "error": "missing_info",
            }, 400

        reminder: ReminderModel = ReminderModelService.retrieve_by_reminder_id(
            reminder_data["reminder_id"], app
        )

        if not reminder.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401
        # TODO: delete the reports of the reminder.
        ReminderModelService.delete(reminder.reminder_id, app, db)
        return {
            "message": "reminder deleted successfully.",
            "reminder_id": reminder_data["reminder_id"],
        }, 200
        # try:
        # except:
        #     return {
        #         "description": "An error occurred while deleting the reminder",
        #         "error": "internal_server_error",
        #     }, 500