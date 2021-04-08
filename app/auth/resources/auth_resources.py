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
from app.shared.db_man.service import DBMan
from ..services.user_model_service import UserModelService
from ..interfaces.user_model_interface import UserModelInterface
from ..models.user_model import UserModel

db = DBMan.get_db()


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
        user_attrs: UserModelInterface = dict(
                                                username = data['username'], 
                                                email = data['email'], 
                                                password = data['password'], 
                                                first_name = data['first_name'], 
                                                last_name = data['last_name']
        
                                            )
        
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
    pass


class AdminRemoveResource(Resource):
    pass


class UserLoginWithEmailResource(Resource):
    pass


class UserLoginWithUsernameResource(Resource):
    pass


class UserLogoutResource(Resource):
    pass


class UpdateUserResource(Resource):
    pass


class DeleteUserResource(Resource):
    pass


class UsersListResource(Resource):
    pass


class UserResource(Resource):
    pass


class Helpers:

    @staticmethod
    def login(user: UserModel):
        pass