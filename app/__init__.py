#region python libraries imports

import sqlite3
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from typing import Iterable
from .auth.interfaces.user_model_interface import UserModelInterface
from .auth.services.user_model_service import UserModelService
from .shared.db_man.service import DBMan, db
from .shared.jwt.token_blocklist_model import TokenBlocklistModel

#endregion


def create_app(env = None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or 'test'])
    api = Api(app)

    jwt = JWTManager(app)
    db.app = app
    db.init_app(app)
    db.create_all(app = app)
    DBMan.create_tables(app, db) #TODO: find a better place for creating tables later

    register_routes(api, app)

    @app.route('/health')
    def healthy():
        return jsonify('healthy')



    #region JWT config methods

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        '''
        This method is used to attach the information of the user to the JWT access token.
        '''
        user = UserModelService.retrieve_by_user_id(identity, app)
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin == 1
        }

    @jwt.token_in_blocklist_loader #callback to chick if the jwt exists in the jwt blocklist database
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = db.session.query(TokenBlocklistModel.id).filter_by(jti = jti).scalar()
        return token is not None

    @jwt.expired_token_loader #going to be called when the toke expires
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token has expired',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader #going to be called when the authentication is not jwt for example auth using jwt instead of Bearer when using flask_jwt_extended
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader #going to be called when they don't send us a jwt at all 
    def missing_token_callback(str):
        return  jsonify({
            'description': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader #going to be called when the token is not fresh and a fresh one is needed
    def token_not_fresh_callback():
        return  jsonify({
            'description': 'The token is not fresh',
            'error': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader #the toke has been revoked for example if the user is logged out
    def revoked_token_callback(jwt_header, jwt_payload):
        return  jsonify({
            'description': 'The token has been revoked',
            'error': 'token_revoked'
        }), 401

    #endregion
    
    #adding admin
    admin: UserModelInterface = dict(
        username = "admin", 
        is_admin = 1, 
        email = "abdelaziz.y.rashed@gmail.com", 
        password = "admin", 
        first_name = "Abdelaziz", 
        last_name = "Rashed"
    )

    UserModelService.create(admin, app, db)

    return app


