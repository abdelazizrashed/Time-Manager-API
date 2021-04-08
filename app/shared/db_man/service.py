import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Iterable


class DBMan:

    @staticmethod
    def get_db():
        db = SQLAlchemy()
        return db

    @staticmethod
    def execute_sql_query(app: Flask, query: str, params: Iterable = ()):
        '''
        This method takes an SQLite query and execute it and returns the rows.
        '''
        connection = sqlite3.connect(app.config['SQLITE_DB_FILE_NAME'])
        curser = connection.cursor()

        result = curser.execute(query, params)

        rows = result.fetchall()
        connection.commit()
        connection.close()

        return rows

    @staticmethod
    def create_tables(app:Flask, db: SQLAlchemy):
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
                        is_admin INTEGER DEFAULT 0,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL
                    );
                    """
            DBMan.execute_sql_query(app, query)

            query = """
                    CREATE TABLE IF NOT EXISTS Colors(
                        color_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        color_value TEXT NOT NULL
                    );
                    """
            DBMan.execute_sql_query(app, query)

            query = """
                    CREATE TABLE IF NOT EXISTS TasksLists(
                        list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_title TEXT NOT NULL
                    );
                    """
            DBMan.execute_sql_query(app, query)

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
            DBMan.execute_sql_query(app, query)

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
            DBMan.execute_sql_query(app, query)

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
            DBMan.execute_sql_query(app, query)

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
            DBMan.execute_sql_query(app, query)

            query = """
                    CREATE TABLE IF NOT EXISTS ReminderTimeSlots(
                        time TEXT NOT NULL,
                        repeat TEXT DEFAULT NULL,
                        reminder TEXT DEFAULT NULL,
                        reminder_id INTEGER NOT NULL,
                        FOREIGN KEY (reminder_id) REFERENCES Reminders(reminder_id)
                    );
                    """
            DBMan.execute_sql_query(app, query)

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
            DBMan.execute_sql_query(app, query)

        else:
            db.create_all(app = app)

        

    @staticmethod
    def drop_tables(app: Flask, db:SQLAlchemy):
        '''
        This method deletes all tables (drop_all).
        '''
        if app.config["DEBUG"] or app.config["TESTING"]:
            query = """
                    select 'drop table ' || name || ';' from sqlite_master
                    where type = 'table';
                    """
            execute_sql_query(app, query)
        else:
            db.drop_all(app = app)
            db.session.commit()