from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .models import ReportModel
from .interfaces import ReportInterface
from ..db_man.service import DBMan


class ReportService:
    @staticmethod
    def json(report: ReportModel):
        """
        This method return the report object in JSON format.
        """
        return {
            "report_id": report.report_id,
            "time_started": report.time_started,
            "time_finished": report.time_finished,
            "event_id": report.event_id,
            "task_id": report.task_id,
            "reminder_id": report.reminder_id,
            "user_id": report.user_id,
        }

    @staticmethod
    def retrieve_by_report_id(report_id: int, app: Flask) -> ReportModel:
        """
        This method returns all the reports that belong to a specific user
        """
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = "SELECT * FROM Reports WHERE report_id = ?;"

            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (report_id,)))
            for row in rows_n_rowid[1]:
                report: ReportModel = ReportModel()
                return report.update(
                    dict(
                        report_id=row[0],
                        time_started=row[1],
                        time_finished=row[2],
                        event_id=row[3],
                        task_id=row[4],
                        reminder_id=row[5],
                        user_id=row[6],
                    )
                )

        else:
            return ReportModel.query.filter_by(report_id=report_id).fetchone()

    @staticmethod
    def retrieve_all_by_user_id(user_id: int, app: Flask) -> List[ReportModel]:
        """
        This method returns all the reports that belong to a specific user
        """
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = "SELECT * FROM Reports WHERE user_id = ?;"

            rows_n_rowid = list(DBMan.execute_sql_query(app, query, (user_id,)))
            reports: List[ReportModel] = []
            for row in rows_n_rowid[1]:
                report: ReportModel = ReportModel()
                reports.append(
                    report.update(
                        dict(
                            report_id=row[0],
                            time_started=row[1],
                            time_finished=row[2],
                            event_id=row[3],
                            task_id=row[4],
                            reminder_id=row[5],
                            user_id=row[6],
                        )
                    )
                )
            return reports
        else:
            return ReportModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def start_an_event(
        event_id: int, user_id: int, time: str, app: Flask, db: SQLAlchemy
    ) -> ReportModel:
        """
        This method is called when an event is started.
        It sets the start time of the event
        """
        report_attrs: ReportInterface = dict(
            time_started=time, event_id=event_id, user_id=user_id
        )
        report: ReportModel = ReportModel()
        report.update(report_attrs)
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    INSERT INTO Reports (time_started, event_id, user_id)
                    VALUES (?, ?, ?)
                    """
            rows_n_rowid = list(
                DBMan.execute_sql_query(app, query, (time, event_id, user_id))
            )
            return report.update(dict(report_id=rows_n_rowid[0]))
        else:
            db.session.add(report)
            db.session.commit()
            return report

    @staticmethod
    def finish_an_event(
        report_id: int, time: str, app: Flask, db: SQLAlchemy
    ) -> ReportModel:
        """
        This method is called when an event is needed to be finished.
        It sets the finish time of the event as well as is_completed to be true.
        """
        updates: ReportInterface = dict(time_finished=time)
        report: ReportModel = ReportService.retrieve_by_report_id(report_id, app)
        if not report:
            return None
        report.update(updates)
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    UPDATE Reports
                    SET time_finished = ?
                    WHERE report_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (time, report_id))
        else:
            db.session.commit()
        return report

    @staticmethod
    def finish_a_reminder(
        reminder_id: int, user_id: int, time: str, app: Flask, db: SQLAlchemy
    ) -> ReportModel:
        """
        This method register a reminder as completed by setting the finish time to the time given
        and is_completed to true.
        """
        report_attrs: ReportInterface = dict(
            time_finished=time, reminder_id=reminder_id, user_id=user_id
        )
        report: ReportModel = ReportModel()
        report.update(report_attrs)
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    INSERT INTO Reports (time_finished, reminder_id, user_id)
                    VALUES (?, ?, ?)
                    """
            rows_n_rowid = list(
                DBMan.execute_sql_query(app, query, (time, reminder_id, user_id))
            )
            return report.update(dict(report_id=rows_n_rowid[0]))
        else:
            db.session.add(report)
            db.session.commit()
            return report

    @staticmethod
    def start_a_task(
        task_id: int, user_id: int, time: str, app: Flask, db: SQLAlchemy
    ) -> ReportModel:
        """
        This method is called when an event is started.
        It sets the start time of the event
        """
        report_attrs: ReportInterface = dict(
            time_started=time, task_id=task_id, user_id=user_id
        )
        report: ReportModel = ReportModel()
        report.update(report_attrs)
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    INSERT INTO Reports (time_started, task_id, user_id)
                    VALUES (?, ?, ?)
                    """
            rows_n_rowid = list(
                DBMan.execute_sql_query(app, query, (time, task_id, user_id))
            )
            return report.update(dict(report_id=rows_n_rowid[0]))
        else:
            db.session.add(report)
            db.session.commit()
            return report

    @staticmethod
    def finish_a_task(
        report_id: int, time: str, app: Flask, db: SQLAlchemy
    ) -> ReportModel:
        """
        This method is called when an event is needed to be finished.
        It sets the finish time of the event as well as is_completed to be true.
        """
        updates: ReportInterface = dict(time_finished=time)
        report: ReportModel = ReportService.retrieve_by_report_id(report_id, app)
        if not report:
            return None
        report.update(updates)
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    UPDATE Reports
                    SET time_finished = ?
                    WHERE report_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (time, report_id))
        else:
            db.session.commit()
        return report
