from typing import Dict, List

from app import db
from app import execute_sql_query
from app.auth.models.user_model import UserModel
from app.auth.interfaces.user_model_interface import  UserModelInterface

class UserModelService:
    @staticmethod
    def json(user: UserModel):
        '''
        This method returns the object in json format.
        '''
        #TODO: a second thought
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    

    #region DB CURD methods

    @staticmethod
    def create(user_attrs: UserModelInterface, app) -> UserModel:
        '''
        This method saves the a user with the attributes based to the method to the database and return the new user.
        If it already exists it will just update it.
        '''
        new_user = UserModel(**user_attrs)
        if UserModelService.retrieve_by_user_id(new_user.user_id, app):
            UserModelService.update(new_user, user_attrs, app)
        else:
            if app.config['DEBUG'] or app.config['TESTING']:
                query = """
                        INSERT INTO Users VALUES (NULL, ?, ?, ?, ?, ?);
                        """
                execute_sql_query(
                    app, 
                    query,
                    (
                    new_user.username, 
                    new_user.password, 
                    new_user.email, 
                    new_user.first_name, 
                    new_user.last_name
                    ) 
                )
            else:
                db.session.add(new_user)
                db.session.commit()
        return new_user

    @staticmethod
    def update(user: UserModel, updates: UserModelInterface, app) -> UserModel:
        '''
        This method updates the existing user with the new updates in the database.
        If the user does not exist in the database it will insert it to the database
        '''
        if not UserModelService.retrieve_by_user_id(user.user_id, app):
            UserModelService.create(updates, app)
        else:
            if app.config['DEBUG'] or app.config['TESTING']:
                user.update(updates)
                query = """
                        UPDATE Users
                        SET username = ?, password = ?, email = ?, first_name = ?, last_name = ?
                        WHERE user_id = ?;
                        """
                execute_sql_query(app, query, (
                    user.username, 
                    user.password, 
                    user.email, 
                    user.first_name, 
                    user.last_name,
                    user.user_id
                    )
                )
            else:
                user.update(updates)
                db.session.commit()
        return user

    
    @staticmethod
    def delete(app, db, user_id: int) -> int:
        '''
        This method deletes a user and return his/her id.
        If nothing could be found it will return None
        '''
        user = UserModelService.retrieve_by_user_id(user_id)
        if user:
            if app.config['DEBUG'] or app.config['TESTING']: 
                query = 'DELETE FROM Events WHERE event_id = ?;'
                execute_sql_query(app, query, (user_id,))
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
            result = execute_sql_query(query, (username))

            row = result.fetchone()
            if row:
                user = UserModel(*row)
            else:
                user = None

            return user

        else:
            return UserModel.query.filter_by(username = username).first()

    @staticmethod
    def retrieve_by_user_id(user_id: int, app) -> UserModel:
        '''
        This method searchs the database for a user by its user_id 
        and return the user in the form of UserModel object.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'SELECT * FROM Users WHERE user_id = ?;'

            rows = execute_sql_query(app, query, (user_id,))
            for row in rows:
                if row:
                    return UserModel(*row)
                else:
                    return None

        else:
            return UserModel.query.filter_by(user_id = user_id).first()

    @staticmethod
    def retrieve_by_email(email: str, app) -> UserModel:
        '''
        This method searchs the database for a user by its email 
        and returns the user in the form of a UserModel object.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:

            query = 'SELECT * FROM Users WHERE email = ?;'

            result = execute_sql_query(app = app, query = query, params = (email,))
            row = result.fetchone()
            if row:
                user = UserModel(*row)
            else:
                user = None

            return user

        else:
            return UserModel.query.filter_by(email = email).first()

    @staticmethod
    def retrieve_all(app) -> List[UserModel]:
        '''
        This method retieve all the user and return them in the form of list.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    SELECT * FROM Users;
                    """
            result = execute_sql_query(app, query)
            rows = result.fetchall()
            users: List[UserModel] = []
            for row in rows:
                user = UserModel(*row)
                users.append(user)
            return users
        else:
            return UserModel.query.all()
    #endregion

    #endregion