from flask import Flask
from flask_restful import Api
from .auth_resources import *

#TODO: remove the scripts from their separate directories into the main module directory

def register_routes(api: Api, app: Flask):
    api.add_resource(UserRegisterResource, '/auth/register', resource_class_kwargs=dict(app = app))
    api.add_resource(AdminRegisterResource, "/auth/admin-register", resource_class_kwargs=dict(app = app))
    api.add_resource(AdminRemoveResource, "/auth/admin-remove", resource_class_kwargs=dict(app = app))
    api.add_resource(UserLoginWithEmailResource, "/auth/login-with-email", resource_class_kwargs=dict(app = app))
    api.add_resource(UserLoginWithUsernameResource, "/auth/login-with-username", resource_class_kwargs=dict(app = app))
    api.add_resource(UserLogoutResource, "/auth/logout", resource_class_kwargs=dict(app = app))
    api.add_resource(UpdateUserResource, "/auth/update-user", resource_class_kwargs=dict(app = app))
    api.add_resource(DeleteUserResource, '/auth/delete-user', resource_class_kwargs=dict(app = app))
    api.add_resource(UsersListResource, '/auth/users', resource_class_kwargs=dict(app = app))
    api.add_resource(UserResource, '/auth/user', resource_class_kwargs=dict(app = app))
    api.add_resource(TokenRefreshResource, '/auth/refresh', resource_class_kwargs=dict(app = app))