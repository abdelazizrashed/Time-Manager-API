#region python liberaries imports

import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

#endregion

#region Custom liberaries imports

import db_man as db
from config_module import DevelopmentConfig
# from db_man import db_url

#endregion

#region Setup the application variable and config

app = Flask(__name__)

app.secret_key = 'secret_key'

api = Api(app)


if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)

    if app.config['DEBUG']:
        db.DBMan.create_tables()

    app.run(debug = True)