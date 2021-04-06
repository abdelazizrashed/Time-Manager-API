#region python liberaries imports

import sqlite3
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

#endregion

db = SQLAlchemy()


def create_app(env = None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or 'test'])
    api = Api(app)

    register_routes(api, app)
    db.init_app(app)

    @app.route('/health')
    def healthy():
        return jsonify('healthy')

    create_tables(app) #TODO: find a better place for creating tables later

    return app


def execute_sql_query(app, query, params = ()):
        '''
        This method takes an SQLite query and execute it and returns the result.
        '''
        connection = sqlite3.connect(app.config['SQLITE_DB_FILE_NAME'])
        curser = connection.cursor()

        result = curser.execute(query, params)

        connection.commit()
        connection.close()

        return result

def create_tables(app):
    '''
    In case the mode of running this app is testing or debugging, 
    this method will create sqlite database tables in local sqlite database server.
    If this is a production server, it will create tables using SQLAlchemy.
    '''
    if app.config["DEBUG"] or app.config["TESTING"]: 
        query = """
                CREATE TABLE IF NOT EXISTS Users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS Colors(
                    color_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    color_value TEXT NOT NULL
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS TasksLists(
                    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    list_title TEXT NOT NULL
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS Events(
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_title TEXT NOT NULL,
                    event_description TEXT DEFAULT NULL,
                    is_completed INTEGER DEFAULT 0,
                    user_id INTEGER NOT NULL,
                    color_id INTEGER NOT NULL,
                    parent_event_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (color_id) REFERENCES Colors(color_id),
                    FOREIGN KEY (parent_event_id) REFERENCES Events(event_id)
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS EventsTimeSlots(
                    time_from TEXT NOT NULL,
                    time_to TEXT NOT NULL,
                    location TEXT DEFAULT NULL,
                    repeat TEXT DEFAULT NULL,
                    reminder TEXT DEFAULT NULL, 
                    event_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (event_id) REFERENCES Events(event_id)
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS Tasks(
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_title TEXT NOT NULL,
                    task_description TEXT,
                    time_from TEXT NOT NULL,
                    time_to TEXT NOT NULL,
                    time_started TEXT,
                    time_finished TEXT,
                    is_completed INTEGER DEFAULT 0,
                    repeat TEXT DEFAULT NULL,
                    reminder TEXT DEFAULT NULL,
                    list_id INTEGER NOT NULL,
                    color_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    parent_event_id INTEGER DEFAULT NULL,
                    parent_task_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (list_id) REFERENCES TasksList(list_id),
                    FOREIGN KEY (color_id) REFERENCES Colors(color_id),
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (parent_event_id) REFERENCES Events(event_id),
                    FOREIGN KEY (parent_task_id) REFERENCES Tasks(task_id)
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS Reminders(
                    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reminder_title TEXT NOT NULL,
                    reminder_description TEXT DEFAULT NULL,
                    is_completed INTEGER DEFAULT 0,
                    user_id INTEGER NOT NULL,
                    color_id INTEGER NOT NULL,
                    parent_event_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (color_id) REFERENCES Colors(color_id),
                    FOREIGN KEY (parent_event_id) REFERENCES Event(event_id)
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS ReminderTimeSlots(
                    time TEXT NOT NULL,
                    repeat TEXT DEFAULT NULL,
                    reminder TEXT DEFAULT NULL,
                    reminder_id INTEGER NOT NULL,
                    FOREIGN KEY (reminder_id) REFERENCES Reminders(reminder_id)
                );
                """
        execute_sql_query(app, query)

        query = """
                CREATE TABLE IF NOT EXISTS Reports(
                    time_started TEXT DEFAULT NULL,
                    time_finished TEXT DEFAULT NULL,
                    event_id INTEGER DEFAULT NULL,
                    task_id INTEGER DEFAULT NULL, 
                    reminder_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (event_id) REFERENCES Events(event_id),
                    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
                    FOREIGN KEY (reminder_id) REFERENCES Reminders(reminder_id)
                );
                """
        execute_sql_query(app, query)

    else:
        db.create_all()