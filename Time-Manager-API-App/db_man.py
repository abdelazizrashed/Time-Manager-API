import sqlite3
from typing import Iterable
from flask_sqlalchemy import SQLAlchemy
from config_module import Config

# import app 



class DBMan:

    #Local DB url that can be used anywhere else
    db_url = Config.sqlite_db_name
    
    #The SQLAlchemy DB manager to be used anywhere in the code
    db = SQLAlchemy()

    def __init__(self):
        pass

    @classmethod
    def create_tables(cls):
        if True: #TODO: change it later to app.config['DEBUG'] or something similar to check if this is development
            connection = sqlite3.connect(cls.db_url)
            curser = connection.cursor()
            #TODO: refactor the queries
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
            curser.execute(query)

            query = """
                    CREATE TABLE IF NOT EXISTS Colors(
                        color_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        color_value TEXT NOT NULL
                    );
                    """
            curser.execute(query)

            query = """
                    CREATE TABLE IF NOT EXISTS TasksLists(
                        list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_title TEXT NOT NULL
                    );
                    """
            curser.execute(query)

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
            curser.execute(query)

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
            curser.execute(query)

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
            curser.execute(query)

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
            curser.execute(query)

            query = """
                    CREATE TABLE IF NOT EXISTS ReminderTimeSlots(
                        time TEXT NOT NULL,
                        repeat TEXT DEFAULT NULL,
                        reminder TEXT DEFAULT NULL,
                        reminder_id INTEGER NOT NULL,
                        FOREIGN KEY (reminder_id) REFERENCES Reminders(reminder_id)
                    );
                    """
            curser.execute(query)
            #TODO:Change the name from logs to reports
            query = """
                    CREATE TABLE IF NOT EXISTS Logs(
                        time_started TEXT DEFAULT NULL,
                        time_finished TEXT DEFAULT NULL,
                        event_id INTEGER DEFAULT NULL FOREIGN KEY REFERENCES Events(event_id),
                        task_id INTEGER DEFAULT NULL FOREIGN KEY REFRENCES Tasks(task_id),
                        reminder_id INTEGER DEFAULT NULL FOREIGN KEY REFRENCES Reminders(reminder_id)
                    );
                    """

            connection.commit()
            connection.close()
        else:
            #TODO: create tables with SQLAlchemy
            pass

    @classmethod
    def execute_query(cls, query, params: Iterable):
        '''
        This method tasks and SQL query and execute it and returns the result.
        '''
        connection = sqlite3.connect(db_url)
        curser = connection.cursor()

        result = curser.execute(query, params)

        connection.commit()
        connection.close()

        return result
