from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, List
from app.shared.db_man.service import DBMan
from app.auth.user_model import UserModel
from app.auth.user_model_interface import  UserModelInterface

class UserModelService:
    @staticmethod
    def json(user: UserModel):
        '''
        This method returns the object in JSON format.
        '''
        #TODO: a second thought
        return {
            'user_id': user.user_id,
            'username': user.username,
            'is_admin': user.is_admin,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    

    #region DB CURD methods

    @staticmethod
    def create(user_attrs: UserModelInterface, app: Flask, db: SQLAlchemy) -> UserModel:
        '''
        This method saves the a user with the attributes based to the method to the database and return the new user.
        If it already exists it will just update it.
        '''
        new_user = UserModel()
        new_user.update(user_attrs)
        if UserModelService.retrieve_by_username(new_user.username, app):
            return {
                'description': "User with this username already exists",
                'error': "username_exists"
            }
        elif  UserModelService.retrieve_by_email(new_user.email, app):
            return {
                'description': "User with this email already exists",
                'error': "email_exists"
            }
        else:
            if app.config['DEBUG'] or app.config['TESTING']:
                query = """
                        INSERT INTO Users (username, is_admin, password, email, first_name, last_name) 
                        VALUES (?, ?, ?, ?, ?, ?);
                        """
                DBMan.execute_sql_query(
                    app, 
                    query,
                    (
                    new_user.username,
                    new_user.is_admin,
                    new_user.password, 
                    new_user.email, 
                    new_user.first_name, 
                    new_user.last_name
                    ) 
                )
            else:
                db.session.add(new_user)
                db.session.commit()
        return UserModelService.retrieve_by_email(new_user.email, app) or UserModelService.retrieve_by_username(new_user.username, app)

    @staticmethod
    def update(user: UserModel, updates: UserModelInterface, app: Flask, db:SQLAlchemy) -> UserModel:
        '''
        This method updates the existing user with the new updates in the database.
        If the user does not exist in the database it will insert it to the database
        '''
        user.update(updates)
        if not UserModelService.retrieve_by_user_id(user.user_id, app):
            return UserModelService.create(updates, app, db)
        
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    UPDATE Users
                    SET username = ?, password = ?, email = ?, first_name = ?, last_name = ?
                    WHERE user_id = ?;
                    """
            DBMan.execute_sql_query(app, query, (
                user.username, 
                user.password, 
                user.email, 
                user.first_name, 
                user.last_name,
                user.user_id
                )
            )
        else:
            db.session.commit()
        return user

    
    @staticmethod
    def delete(app: Flask, db: SQLAlchemy, user_id: int) -> int:
        '''
        This method deletes a user and return his/her id.
        If nothing could be found it will return None
        '''
        user = UserModelService.retrieve_by_user_id(user_id, app)
        if user:
            if app.config['DEBUG'] or app.config['TESTING']: 
                query = 'DELETE FROM Users WHERE user_id = ?;'
                DBMan.execute_sql_query(app, query, (user_id,))
                return user_id
            else:
                db.session.delete(user)
                db.session.commit()
                return user_id
        else:
            return None

    #region retrieving users

    @staticmethod
    def retrieve_by_username(username: str, app) -> UserModel:
        '''
        This method search in the database for a user by its username 
        and return the user in the form of a UserModel object.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'SELECT * FROM Users WHERE username = ?;'
            rows = DBMan.execute_sql_query(app, query, (username,))

            for row in rows:
                if row:
                    user = UserModel()
                    return user.update(changes = dict(
                      user_id = row[0],
                      username = row[1],
                      is_admin = row[2],
                      password = row[3],
                      email = row[4],
                      first_name = row[5],
                      last_name = row[6]  
                    ))

            
            return None

        else:
            return UserModel.query.filter_by(username = username).first()

    @staticmethod
    def retrieve_by_user_id(user_id: int, app) -> UserModel:
        '''
        This method searches the database for a user by its user_id 
        and return the user in the form of UserModel object.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'SELECT * FROM Users WHERE user_id = ?;'

            rows = DBMan.execute_sql_query(app, query, (user_id,))
            for row in rows:
                if row:
                    user = UserModel()
                    return user.update(changes = dict(
                      user_id = row[0],
                      username = row[1],
                      is_admin = row[2],
                      password = row[3],
                      email = row[4],
                      first_name = row[5],
                      last_name = row[6]  
                    ))
            
            return None

        else:
            return UserModel.query.filter_by(user_id = user_id).first()

    @staticmethod
    def retrieve_by_email(email: str, app) -> UserModel:
        '''
        This method searches the database for a user by its email 
        and returns the user in the form of a UserModel object.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'SELECT * FROM Users WHERE email = ?;'

            rows = DBMan.execute_sql_query(app = app, query = query, params = (email,))
            for row in rows:
                if row:
                    user = UserModel()
                    return user.update(changes = dict(
                      user_id = row[0],
                      username = row[1],
                      is_admin = row[2],
                      password = row[3],
                      email = row[4],
                      first_name = row[5],
                      last_name = row[6]  
                    ))
            
            return None

        else:
            return UserModel.query.filter_by(email = email).first()

    @staticmethod
    def retrieve_all(app) -> List[UserModel]:
        '''
        This method retrieve all the user and return them in the form of list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    SELECT * FROM Users;
                    """
            rows = DBMan.execute_sql_query(app, query)
            users: List[UserModel] = []
            for row in rows:
                user = UserModel()
                users.append(user.update(changes = dict(
                      user_id = row[0],
                      username = row[1],
                      is_admin = row[2],
                      password = row[3],
                      email = row[4],
                      first_name = row[5],
                      last_name = row[6]  
                    ))) 
            return users
        else:
            return UserModel.query.all()
    #endregion

    #endregion