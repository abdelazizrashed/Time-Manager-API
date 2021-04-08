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
from app.shared.db_man.service import DBMan, db
from ..services.user_model_service import UserModelService
from ..interfaces.user_model_interface import UserModelInterface
from ..models.user_model import UserModel


#region Request Parser arguments

_user_parser = reqparse.RequestParser()

_user_parser.add_argument(
    'username',
    type = str, 
    required = True, 
    help = "A unique username for the user that identifies him/ her"
)

_user_parser.add_argument(
    'password', 
    type = str, 
    required = True, 
    help = "The password of the user which will be used to authenticate him/ her"
)


_user_parser.add_argument(
    'email',
    type = str, 
    required = True, 
    help = "A unique email for the user that will be attached to the account."
)

_user_parser.add_argument(
    'first_name', 
    type = str, 
    required = True, 
    help = "The first name of the user"
)

_user_parser.add_argument(
    'last_name',
    type = str, 
    required = True, 
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
        update: UserModelInterface = dict(is_admin = 1)

        user =  UserModelService.update(user, update, self.app, db)

        return UserModelService.json(user)



class AdminRemoveResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UserLoginWithEmailResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UserLoginWithUsernameResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UserLogoutResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UpdateUserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class DeleteUserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UsersListResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class UserResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class TokenRefreshResource(Resource):

    
    def __init__(self, app: Flask):
        self.app = app
    pass


class Helpers:

    @staticmethod
    def login(user: UserModel):
        pass