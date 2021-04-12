from flask import Flask
from flask_restful import Resource, reqparse
from werkzeug.security import  safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required,
    get_jwt_identity,
    get_jwt
    )
from datetime import datetime, timezone
from typing import List
from app.shared.db_man.service import DBMan, db
from app.shared.jwt.token_blocklist_model import TokenBlocklistModel
from .user_model_service import UserModelService
from .user_model_interface import UserModelInterface
from .user_model import UserModel


#region Request Parser arguments

_user_parser = reqparse.RequestParser()

_user_parser.add_argument(
    'user_id', 
    type=str, 
    help="A unique number that identifies the user in the database"
)

_user_parser.add_argument(
    'username',
    type = str, 
    help = "A unique username for the user that identifies him/ her"
)

_user_parser.add_argument(
    'password', 
    type = str,  
    help = "The password of the user which will be used to authenticate him/ her"
)


_user_parser.add_argument(
    'email',
    type = str,  
    help = "A unique email for the user that will be attached to the account."
)

_user_parser.add_argument(
    'first_name', 
    type = str,  
    help = "The first name of the user"
)

_user_parser.add_argument(
    'last_name',
    type = str,  
    help = "The last name of the user."
)

#endregion



class UserRegisterResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app

    def post(self):
        data = _user_parser.parse_args()
        if UserModelService.retrieve_by_username(data['username'], self.app):
            return {
                'description': "A user with this username already exists.",
                'error': "username_exists"
            }, 400
        if UserModelService.retrieve_by_email(data['email'], self.app):
            return {
                'description': "A user with this email already exists.",
                'error': 'email_exists'
            }, 400
        user_attrs: UserModelInterface = dict(data)
        
        if self.app:
            user = UserModelService.create(user_attrs, self.app, db)

            access_token = create_access_token(identity= user.user_id, fresh= True)
            refresh_token = create_refresh_token(identity= user.user_id)

            return {
                'message': 'User created successfully.',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        return 500
        

class AdminRegisterResource(Resource):

    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required(fresh= True)
    def post(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return {
                'description': "Admin privileges are required",
                'error': 'admin_required'
            }, 401
        data = _user_parser.parse_args()

        user: UserModel = UserModelService.retrieve_by_user_id(data['user_id'], self.app)
        if not user:
            return {
                'description': "The user_id is incorrect or the user doesn't exist.",
                'error': 'invalid_user_id'
            }, 404
        update: UserModelInterface = dict(is_admin = 1)

        user =  UserModelService.update(user, update, self.app, db)

        return {
            'message': "User upgraded to admin successfully",
            "user_data": UserModelService.json(user)
        }



class AdminRemoveResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required(fresh = True)
    def delete(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return {
                'description': "Admin privileges are required",
                'error': 'admin_required'
            }, 401
        data = _user_parser.parse_args()
        user: UserModel = UserModelService.retrieve_by_user_id(data['user_id'], self.app)
        if not user:
            return {
                'description': "The user_id is incorrect or the user doesn't exist.",
                'error': 'invalid_user_id'
            }, 404
        updates: UserModelInterface = dict(is_admin = 0)

        user = UserModelService.update(user, updates, self.app, db)
        
        return {
            'message': "User upgraded to admin successfully",
            "user_data": UserModelService.json(user)
        }



class UserLoginWithEmailResource(Resource):


    def __init__(self, app: Flask):
        self.app = app
    

    def post(self):
        data = _user_parser.parse_args()

        user: UserModel = UserModelService.retrieve_by_email(data['email'], self.app)
        
        if not user:
            return {
                'description': "The email is incorrect or the user doesn't exist",
                'error': "invalid_email"
            }, 404

        return Helpers.login(user, data['password'])


class UserLoginWithUsernameResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app


    def post(self):
        data = _user_parser.parse_args()

        user: UserModel = UserModelService.retrieve_by_username(data['username'], self.app)
        
        if not user:
            return {
                'description': "The username is incorrect or the user doesn't exist",
                'error': "invalid_username"
            }, 404

        return Helpers.login(user, data['password'])


class UserLogoutResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        return Helpers.logout(jti)


class UpdateUserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required(fresh = True)
    def put(self):
        claims = get_jwt()
        data = _user_parser.parse_args()
        user: UserModel = UserModelService.retrieve_by_user_id(data['user_id'], self.app)
        if not int(data['user_id']) == int(claims['user_id']) and not claims['is_admin']:
            return {
                'description': "You need to be the user modifying his/ her information or an admin",
                'error': "invalid_credentials"
            }, 401

        updates: UserModelInterface = dict()

        if data['username']:
            if data['username'] != user.username:
                if UserModelService.retrieve_by_username(data['username'], self.app):
                    return {
                        "description": "A user with this username already exists",
                        'error': 'username_exists'
                    }, 400

                updates['username'] = data['username']
        if data['password']:
            if data['password'] != user.password:
                updates['password'] = data['password']
            else:
                return {
                    'description': "Your new password can't be the same as your old one",
                    'error': "invalid_password"
                }, 400

        if data['email']:
            if data['email'] != user.email:
                if UserModelService.retrieve_by_email(data['email'], self.app):
                    return{
                        'description': "A user with this email already exists",
                        'error': "email_exists"
                    }, 400
                updates['email'] = data['email']

        if data['first_name']:
            if data['first_name'] != user.first_name:
                updates['first_name'] = data['first_name']
        
        if data['last_name']:
            if data['last_name'] != user.last_name:
                updates['last_name'] = data['last_name']
        if len(updates) == 0:
            return {
                "description": "No new data was provided",
                "error": "no_info"
            }, 404

        new_user: UserModel = UserModelService.update(user, updates, self.app, db)

        return {
            'message': "User data updated successfully",
            "user_data": UserModelService.json(new_user)
        }
        

class DeleteUserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required(fresh = True)
    def delete(self):
        claims = get_jwt()
        data = _user_parser.parse_args()
        #TODO: delete all tasks, events, and reminder that belong to the user.
        user: UserModel = UserModelService.retrieve_by_user_id(data['user_id'], self.app)
        if not int(data['user_id']) == int(claims['user_id']) and not claims['is_admin']:
            return {
                'description': "You need to be the user modifying his/ her information or an admin",
                'error': "invalid_credentials"
            }, 401
        Helpers.logout(claims['jti'])
        try:
            if not UserModelService.delete(self.app, db, user.user_id):
                return {
                    'message': "User couldn't be deleted. The user may not exist"
                }, 404
            return {
                'message': "User deleted successfully."
            }, 200
        except :
            return{
                'description': "Server error when deleting user.",
                'error': 'internal_server_error'
            }, 500



class UsersListResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required(fresh = True)
    def get(self):
        claims = get_jwt()
        if not claims['is_admin']:
            return {
                'description': "Admin privileges are required",
                'error': 'admin_required'
            }, 401
        users: List[UserModel] = UserModelService.retrieve_all(self.app)
        return {
            'users': [UserModelService.json(user) for user in users]
        }



class UserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        data = _user_parser.parse_args()

        if not int(data['user_id']) == int(claims['user_id']) and not claims['is_admin']:
            return {
                'description': "You need to be the user modifying his/ her information or an admin",
                'error': "invalid_credentials"
            }, 401

        if data['user_id']:
            user = UserModelService.retrieve_by_user_id(data['user_id'], self.app)
            if user:
                json = UserModelService.json(user)
                return {
                    "user_info": json
                }, 200
            else:
                return {
                    'description': "The user_id is incorrect or the user doesn't exists",
                    'error': "invalid_user_id"
                }
        if data['username']:
            user = UserModelService.retrieve_by_username(data['username'], self.app)
            if user:
                return {
                    "user_info": UserModelService.json(user)
                }, 200
            else:
                return {
                    'description': "The username is incorrect or the user doesn't exist",
                    'error': "invalid_username"
                }, 404
        if data['email']:
            user = UserModelService.retrieve_by_email(data['email'], self.app)
            if user:
                return {
                    "user_info": UserModelService.json(user)
                }, 200
            else:
                return {
                    'description': "The email is incorrect or the user doesn't exist",
                    'error': "invalid_email"
                }, 404
        return {
            'description': "No user info was supplied. Please make sure to send the user_id, username, or email.",
            'error': "no_info"
        }



class TokenRefreshResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    

    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user, fresh = False)
        return {'access_token': new_token}, 200


class Helpers:

    @staticmethod
    def login(user: UserModel, password):
        if safe_str_cmp(user.password, password):
            access_token = create_access_token(identity= user.user_id, fresh = True)
            refresh_token = create_refresh_token(identity= user.user_id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {
            'description': "The password provided didn't match the user password.",
            'error': "invalid_password"
        }, 401

    @staticmethod
    def logout(jti):
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklistModel(jti = jti, created_at = now))
        db.session.commit()
        return {'message': 'User logged out.'}, 200