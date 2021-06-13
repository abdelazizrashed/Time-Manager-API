from flask import Flask
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from .services import ReportService


class ReportsListResource(Resource):
    def __init__(self, app: Flask):
        self.app = app

    @jwt_required()
    def get(self):
        claims = get_jwt()
        return {
            "reports": [
                ReportService.json(report)
                for report in ReportService.retrieve_all_by_user_id(
                    claims.get("user_id"), self.app
                )
            ]
        }, 200
