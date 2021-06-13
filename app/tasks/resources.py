from flask import Flask
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_sqlalchemy import SQLAlchemy
from ..shared.db_man.service import db
from ..shared.reports.models import ReportModel
from ..shared.reports.services import ReportService
from .models import TasksListModel, TaskModel
from .interfaces import TaskModelInterface, TasksListModelInterface
from .services import TaskModelService, TasksListModelService
import json


class TaskResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        task_data = request.get_json()
        if not task_data.get("task_id"):
            return {"description": "No task id found.", "error": "missing_info"}, 400
        task = TaskModelService.retrieve_by_task_id(task_data["task_id"], self.app)
        if task == None:
            return {"description": "Task couldn't be found", "error": "not_found"}, 404
        if task.user_id != claims.get("user_id"):
            return {
                "description": "You can't access other users events.",
                "error": "invalid_credentials",
            }, 401
        return TaskModelService.json(task), 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        task_data = request.get_json()

        return Helper.create_task(task_data, claims, self.app)

    @jwt_required()
    def put(self):
        claims = get_jwt()
        task_data = request.get_json()

        return Helper.update_task(task_data, claims, self.app)

    @jwt_required()
    def delete(self):
        claims = get_jwt()
        data = request.get_json()

        return Helper.delete_task(data, claims, self.app)


class TasksResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        return {
            "tasks": [
                TaskModelService.json(task)
                for task in TaskModelService.retrieve_tasks_by_user_id(
                    claims.get("user_id"), self.app
                )
            ]
        }, 200

    @jwt_required()
    def post(self):
        return {"message": "This request isn't supported yet"}, 405

    @jwt_required()
    def put(self):
        return {"message": "This request isn't supported yet"}, 405

    @jwt_required()
    def delete(self):
        return {"message": "This request isn't supported yet"}, 405


class TasksListResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        data = request.get_json()
        if not data.get("list_id"):
            return {
                "description": "You need to supply the list id of the list you need to get",
                "error": "missing_info",
            }, 400
        return (
            TasksListModelService.json(
                TasksListModelService.retrieve_by_list_id(data.get("list_id"), self.app)
            ),
            200,
        )

    @jwt_required()
    def post(self):
        claims = get_jwt()
        data = request.get_json()
        if not data.get("list_title"):
            return {
                "description": "The list can not be created without list title",
                "error": "missing_info",
            }, 400
        return {
            "message": "The list created successfully",
            "list": TasksListModelService.json(
                TasksListModelService.create(
                    dict(
                        list_title=data.get("list_title"), user_id=claims.get("user_id")
                    ),
                    self.app,
                    db,
                )
            ),
        }, 201


class TasksListsResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        return {
            "lists": [
                TasksListModelService.json(_list)
                for _list in TasksListModelService.retrieve_lists_by_user_id(
                    claims.get("user_id"), self.app
                )
            ]
        }


class StartTaskResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        claims = get_jwt()
        data = request.get_json()

        if not data["task_id"]:
            return {
                "description": "You need to supply the task_id of the task needed to be registered as started",
                "error": "missing_info",
            }, 400

        if not data["time"]:
            return {
                "description": "The start time of the task must be supplied as time",
                "error": "missing_info",
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_task_id(
            data["task_id"], self.app
        )

        if not task:
            return {"description": "Task not found", "error": "not_found"}, 404

        if not task.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401

        report: ReportModel = ReportService.start_a_task(
            task.task_id, claims.get("user_id"), data["time"], self.app, db
        )
        return {
            "message": "Task registered as started successfully",
            "report": ReportService.json(report),
        }, 200
        # try:
        # except:
        #     return {
        #         "description": "Failure will registering the task",
        #         "error": "internal_server_error",
        #     }, 500


class FinishTaskResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def post(self):
        claims = get_jwt()
        data = request.get_json()

        if not data.get("task_id"):
            return {
                "description": "You need to supply the task_id of the task needed to be registered as finished",
                "error": "missing_info",
            }, 400

        if not data.get("report_id"):
            return {
                "description": "You need to supply the report_id of the report that this event is register as started in.",
                "error": "missing_info",
            }, 400

        if not data.get("time"):
            return {
                "description": "The finish time of the task must be supplied as time",
                "error": "missing_info",
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_task_id(
            data["task_id"], self.app
        )

        if not task:
            return {"description": "Task not found", "error": "not_found"}, 404

        if not task.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401

        report: ReportModel = ReportService.finish_a_task(
            data["report_id"], data["time"], self.app, db
        )
        return {
            "message": "Task registered as finished successfully",
            "report": ReportService.json(report),
        }, 200
        # try:
        # except:
        #     return {
        #         "description": "Failure will registering the task",
        #         "error": "internal_server_error",
        #     }, 500


class Helper:
    @staticmethod
    def create_task(task_data: dict, claims: dict, app: Flask):

        if not task_data["task_title"]:
            return {
                "description": "The task needs a title",
                "error": "missing_info",
            }, 400

        if not task_data["time_from"] or not task_data["time_to"]:
            return {
                "description": "The task needs a start time and a finish time",
                "error": "missing_info",
            }, 400

        if not task_data["list_id"]:
            return {
                "description": "The task needs to belong to a list",
                "error": "missing_info",
            }, 400

        if not task_data["color_id"]:
            return {
                "description": "The task must have an identifying color",
                "error": "missing_info",
            }, 400

        task_attrs: TaskModelInterface = dict(
            task_title=task_data.get("task_title"),
            task_description=task_data.get("task_description"),
            time_from=task_data.get("time_from"),
            time_to=task_data.get("time_to"),
            time_started=task_data.get("time_started"),
            time_finished=task_data.get("time_finished"),
            is_complete=task_data.get("is_complete"),
            reminder=json.dumps(task_data.get("reminder")),
            repeat=task_data.get("repeat"),
            list_id=task_data.get("list_id"),
            color_id=task_data.get("color_id"),
            user_id=claims.get("user_id"),
            parent_event_id=task_data.get("parent_event_id"),
            parent_task_id=task_data.get("parent_task_id"),
        )

        task: TaskModel = TaskModelService.create(task_attrs, app, db)
        return {
            "message": "The task created successfully",
            "task": TaskModelService.json(task),
        }, 201

    @staticmethod
    def update_task(task_data: dict, claims: dict, app: Flask):

        if not task_data["task_id"]:
            return {
                "description": "You need to supply the task_id of the task needed to be modified",
                "error": "missing_info",
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_task_id(
            task_data["task_id"], app
        )
        if task == None:
            return Helper.create_task(task_data, claims, app)
        if not task.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401

        updates: TaskModelInterface = dict()
        if task_data.get("task_title"):
            updates.update(task_title=task_data["task_title"])
        if task_data.get("task_description"):
            updates.update(task_description=task_data["task_description"])
        if task_data.get("time_from"):
            updates.update(time_from=task_data["time_from"])
        if task_data.get("time_to"):
            updates.update(time_to=task_data["time_to"])
        if task_data.get("time_started"):
            updates.update(time_started=task_data["time_started"])
        if task_data.get("time_finished"):
            updates.update(time_finished=task_data["time_finished"])
        if task_data.get("is_completed"):
            updates.update(is_completed=task_data["is_completed"])
        if task_data.get("reminder"):
            updates.update(reminder=task_data["reminder"])
        if task_data.get("repeat"):
            updates.update(repeat=task_data["repeat"])
        if task_data.get("color_id"):
            updates.update(color_id=task_data["color_id"])
        if task_data.get("user_id"):
            updates.update(user_id=claims.get("user_id"))
        if task_data.get("parent_event_id"):
            updates.update(parent_event_id=task_data["parent_event_id"])
        if task_data.get("parent_task_id"):
            updates.update(parent_task_id=task_data["parent_task_id"])

        return {
            "message": "Task updated successfully",
            "task": TaskModelService.json(
                TaskModelService.update(task, updates, app, db)
            ),
        }, 200

    @staticmethod
    def delete_task(data: dict, claims: dict, app: Flask):

        if not data["task_id"]:
            return {
                "description": "You need to supply the task_id of the task needed to be deleted",
                "error": "missing_info",
            }, 400

        task: TaskModel = TaskModelService.retrieve_by_task_id(data["task_id"], app)

        if task == None:
            return {"description": "Task couldn't be found", "error": "not_found"}, 404
        if not task.user_id == claims.get("user_id"):
            return {
                "description": "Can't access other users data",
                "error": "invalid_credentials",
            }, 401
        # TODO: delete the reports of the task.
        TaskModelService.delete(task.task_id, app, db)
        return {
            "message": "Task deleted successfully.",
            "task_id": data["task_id"],
        }, 200
        # try:
        # except:
        #     return {
        #         "description": "An error occurred while deleting the task",
        #         "error": "internal_server_error",
        #     }, 500