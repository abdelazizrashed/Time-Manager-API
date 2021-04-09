from app.db_man import DBMan
import sqlite3
import app


class ColorModel(db.Model):

    __tablename__ = "Colors"

    #region SQLAlchemy table columns

    color_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement = True
    )

    color_value = db.Column(
        db.String(50),
        nullable = False
    )

    #endregion

    def __init__(self, color_id, color_value):
        self.color_id = color_id
        self.color_value = color_value
    
    def json(self):
        '''
        This method return the object in JSON format
        '''
        return {
            'color_id': self.color_id,
            'color_value': self.color_value
        }
    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current color to the database.
        If the color already exists it will just update it.
        '''
        if self.find_by_color_id(self.color_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO Colors VALUES (NULL, ?);
                        """
                curser.execute(query, (
                    self.color_value,
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    def update_in_db(self):
        '''
        This method will update the current color in the database with its current values.
        If the color does not exist in the database it will save it.
        '''
        if not self.find_by_color_id(self.user_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE Colors
                        SET color_value = ?
                        WHERE color_id = ?;
                        """
                curser.execute(query, (
                    self.color_value,
                    self.color_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()

    def delete_from_db(self):
        '''
        This method will delete a color from the database only if it exists.
        '''
        if self.find_by_color_id(self.color_id):
            if app.app.config['DEBUG']:
                connection = sqlite3.connect(db_url)
                curser = connection.cursor()

                query = 'DELETE FROM Colors WHERE color_id = ?;'
                curser.execute(query, (self.color_id,))

                connection.commit()
                connection.close()
            else:
                db.session.delete(self)
                db.session.commit()

    @classmethod
    def find_by_color_id(cls, color_id):
        '''
        This method searchs the database for a color with the given color id.
        If the color does not exist it will return None.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM Colors WHERE color_id = ?;'

            result = curser.execute(query, (color_id,))
            row = result.fetchone()
            if row:
                color = cls(*row)
            else:
                color = None

            connection.close()
            return color

        else:
            return cls.query.filter_by(color_id = color_id).first()

    #endregion