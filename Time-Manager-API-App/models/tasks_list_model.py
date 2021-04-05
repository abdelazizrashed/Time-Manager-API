from db_man import db, db_url
import sqlite3
import app


class TasksListModel(db.Model):

    __tablename__ = "TasksLists"

    #region SQLAlchemy table columns

    list_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    list_title = db.Column(
        db.String(50),
        nullable = False
    )

    #endregion

    def __init__(self, list_id, list_title):
        self.list_id = list_id
        self.list_title = list_title
    
    def json(self):
        '''
        This method return the object in JSON format
        '''
        #TODO: a second thougt
        return {
            'list_id': self.list_id,
            'list_title': self.list_title
        }
    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current TasksList to the database.
        If the Tasks List already exists it will just update it.
        '''
        if self.find_by_list_id(self.list_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO TasksLists VALUES (NULL, ?);
                        """
                curser.execute(query, (
                    self.list_title,
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    def update_in_db(self):
        '''
        This method will update the current TasksList in the database with its current values.
        If the TasksList does not exist in the database it will save it.
        '''
        if not self.find_by_list_id(self.list_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE TasksLists
                        SET list_title = ?
                        WHERE list_id = ?;
                        """
                curser.execute(query, (
                    self.list_title,
                    self.list_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()

    def delete_from_db(self):
        '''
        This method will delete the TasksList and its tasks from the database only if it exists.
        '''
        if find_by_list_id(self.color_id):
            if app.app.config['DEBUG']:
                #TODO: delete the tasks the belong to this tasks list
                connection = sqlite3.connect(db_url)
                curser = connection.cursor()

                query = 'DELETE FROM TasksLists WHERE list_id = ?;'
                curser.execute(query, (self.list_id,))

                connection.commit()
                connection.close()
            else:
                 #TODO: delete the tasks the belong to this tasks list
                db.session.delete(self)
                db.session.commit()

    @classmethod
    def find_by_list_id(cls, list_id):
        '''
        This method searchs the database for a list with the given list id.
        If the list does not exist it will return None.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM TasksLIsts WHERE list_id = ?;'

            result = curser.execute(query, (list_id,))
            row = result.fetchone()
            if row:
                new_list = cls(*row)
            else:
                new_list = None

            connection.close()
            return new_list

        else:
            return cls.query.filter_by(list_id = list_id).first()

    #endregion