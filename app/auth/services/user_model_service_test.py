from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from typing import List
from app.test.fixtures import db, app_test, app_prod, setup_sqlite_db
from app import create_tables, execute_sql_query, create_app
from app.config import config_by_name
from ..models.user_model import  UserModel
from ..interfaces.user_model_interface import  UserModelInterface
from ..services.user_model_service import UserModelService



def test_json():
    '''
    Tests that it can convert the object to JSON successfully
    '''
    #arrange
    user1: UserModel = UserModel(user_id = 1, username= 'user1', password= 'asd', email= 'email@email.com', first_name= 'user1', last_name= 'user1_family')
    json = {
        'user_id': 1,
        'username': 'user1',
        'email': 'email@email.com',
        'first_name': 'user1',
        'last_name': 'user1_family'
    }

    #assert
    assert UserModelService.json(user1) == json

def test_create_test(app_test: Flask):
    '''
    Tests that the sqlite part of the method can create a user in the db successfully.
    '''
    #arrange
    setup_sqlite_db(app = app_test, table_name = 'Users')
    user1: UserModelInterface = dict(username= 'user1', password= 'asd', email= 'email@email.com', first_name= 'user1', last_name= 'user1_family', user_id = None)

    #act
    UserModelService.create(user1, app_test)
    query = """
            SELECT * FROM Users;
            """
    rows = execute_sql_query(app = app_test, query = query)

    #assert
    assert len(rows) == 1
    for row in rows:
        user = UserModel(*row)
        for key in user1.keys():
            assert getattr(user, key) == user1[key]

def test_create_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    Tests that the SQLAlchemy part of the method can create the user in the db successfully.
    '''
    #arrange
    user1: UserModelInterface = dict(user_id = 1, username= 'user1', password= 'asd', email= 'email@email.com', first_name= 'user1', last_name= 'user1_family')

    #act
    UserModelService.create(user1, app_prod)
    users: List[UserModel] = UserModel.query.all()

    #assert
    assert len(users) == 1

    for key in user1.keys():
        assert getattr(users[0], key) == user1[key]
    

def test_update_test(app_test: Flask):
    '''
    Tests that the sqlite part of the method can update and existing user successfully.
    '''
    #arrange
    setup_sqlite_db(app_test, 'Users')
    user1: UserModel = UserModel(user_id = 1, username= 'user1', password= 'asd', email= 'email@email.com', first_name= 'user1', last_name= 'user1_family')
    
    query = "DELETE FROM Users;"
    execute_sql_query(app_test, query)

    query = """
            SELECT * FROM Users;
            """
    rows = execute_sql_query(app = app_test, query = query)

    query = """
            INSERT INTO Users 
            VALUES (NULL, ?, ?, ?, ?, ?);
            """
    execute_sql_query(app_test, query, (user1.username, user1.password, user1.email, user1.first_name, user1.last_name))
    
    query = """
            SELECT * FROM Users;
            """
    rows = execute_sql_query(app = app_test, query = query)

    updates: UserModelInterface = dict(password = 'qwe')

    #act 
    UserModelService.update(user1, updates, app_test)
    query = """SELECT * FROM Users;"""
    rows = execute_sql_query(app_test, query)
    
    #assert
    assert len(rows) == 1
    updated_user = UserModel(*rows[0])
    assert updated_user.password == updates['password']

def test_update_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    Tests that the SQLAlchemy part of the method can update an existing user successfully.
    '''
    #arrange

    #act 

    #assert
    pass

def test_delete_test(app_test: Flask):
    '''
    Tests that the sqlite part of the method can delete a user successfully.
    '''
    #arrange

    #act 

    #assert
    pass

def test_delete_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    Tests that the SQLAlchemy part of the method can delete a user successfully.
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_user_id_test(app_test: Flask):
    '''
    SQLite
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_user_id_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    SQLAlchemy
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_username_test(app_test: Flask):
    '''
    SQLite
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_username_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    SQLAlchemy
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_email_test(app_test: Flask):
    '''
    SQLite
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_by_email_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    SQLAlchemy
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_all_test(app_test: Flask):
    '''
    SQLite
    '''
    #arrange

    #act 

    #assert
    pass

def test_retrieve_all_prod(app_prod: Flask, db: SQLAlchemy):
    '''
    SQLAlchemy
    '''
    #arrange

    #act 

    #assert
    pass
#TODO: continue the rest of the function at the same manner and implement them