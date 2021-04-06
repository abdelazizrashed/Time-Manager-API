from db_man import db, db_url
import sqlite3
import app


class UserModel(db.Model):
    __tablename__ = 'Users'

    #region sqlalchemy table columns 
    user_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    username = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )

    password = db.Column(
        db.String(50),
        nullable = False
    )

    email = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )

    first_name = db.Column(
        db.String(50),
        nullable = False
    )

    last_name = db.Column(
        db.String(50),
        nullable = False
    )
    #endregion

    def __init__(self, user_id, username, password, email, first_name, last_name):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        slef.last_name = last_name

    def json(self):
        '''
        This method returns the object in json format.
        '''
        #TODO: a second thought
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
    

    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current user to the database.
        If it already exists it will just update it.
        '''
        if self.find_by_user_id(self.user_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO Users VALUES (NULL, ?, ?, ?, ?, ?);
                        """
                curser.execute(query, (
                    self.username, 
                    self.password, 
                    self.email, 
                    self.first_name, 
                    self.last_name
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    def update_in_db(self):
        '''
        This method updates the the existing user in the database.
        If the user does not exist in the database it will insert it to the database
        '''
        if not self.find_by_user_id(self.user_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE Users
                        SET username = ?, password = ?, email = ?, first_name = ?, last_name = ?
                        WHERE user_id = ?;
                        """
                curser.execute(query, (
                    self.username, 
                    self.password, 
                    self.email, 
                    self.first_name, 
                    self.last_name,
                    self.user_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()


    #region finding a user methods

    @classmethod
    def find_by_username(cls, username):
        '''
        This method search in the database for a user by its username and return a UserModel object.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Users WHERE username = ?;'

            result = curser.execute(query, (username,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None

            connection.close()
            return user

        else:
            return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        '''
        This method searchs the database for a user by its user_id and return a UserModel object
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Users WHERE user_id = ?;'

            result = curser.execute(query, (user_id,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None

            connection.close()
            return user

        else:
            return cls.query.filter_by(user_id = user_id).first()

    @classmethod 
    def find_by_email(cls, email):
        '''
        This method searchs the database for a user by its email and returns a UserModel object.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Users WHERE email = ?;'

            result = curser.execute(query, (email,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None

            connection.close()
            return user

        else:
            return cls.query.filter_by(email = email).first()

    #endregion

    #endregion