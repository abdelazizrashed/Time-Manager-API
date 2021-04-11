from flask import Flask
from sqlalchemy import SQLAlchemy
from .models import ReportModel
from .interfaces import ReportInterface
from ..db_man.service import DBMan


class ReportService:


    @staticmethod
    def json(report: ReportModel):
        '''
        This method return the report object in JSON format.
        '''
        return {
            "report_id": report.reminder_id,
            "time_started": report.time_started,
            "time_finished": report.time_finished,
            "event_id": report.event_id,
            "task_id": report.task_id,
            "reminder_id": report.reminder_id,
            "user_id": report.user_id
        }

    @staticmethod
    def start_an_event(event_id: int, time: str, app: Flask, db: SQLAlchemy) -> ReportModel:
        '''
        This method is called when an event is started. 
        It sets the start time of the event
        '''
        report_attrs: ReportInterface = dict(time_started = time, event_id = event_id)
        report: ReportModel = ReportModel()
        report.update(report_attrs)
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO Reports (time_started, event_id)
                    VALUES (?, ?)
                    """
            DBMan.execute_sql_query(app, query, (time, event_id))
        else:
            db.session.add(report)
            db.session.commit()
        return report

    @staticmethod
    def finish_an_evnet(report_id: int, time: str, app: Flask, db: SQLAlchemy) -> ReportModel:
        '''
        This method is called when an event is needed to be finished.
        It sets the finish time of the event as well as is_completed to be true.
        '''
        report_attrs: ReportInterface = dict(time_started = time)
        report: ReportModel = ReportModel()
        report.update(report_attrs)
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    UPDATE Reports
                    SET time_finished = ?
                    WHERE report_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (time, report_id))
        else:
            db.session.add(report)
            db.session.commit()
        return report
        
            