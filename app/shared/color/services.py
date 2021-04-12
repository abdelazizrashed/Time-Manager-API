from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import List
from ..db_man.service import DBMan
from .models import ColorModel
from .interfaces import ColorInterface


class ColorService:

    @staticmethod
    def json(color: ColorModel):
        '''
        This method return the object in JSON format
        '''
        return {
            'color_id': color.color_id,
            'color_value': color.color_value
        }
    #region DB methods

    @staticmethod
    def create(color_attrs: ColorInterface, app: Flask, db: SQLAlchemy) -> ColorModel:
        '''
        This method saves the current color to the database.
        If the color already exists it will just update it.
        '''
        color: ColorModel = ColorModel()
        color.update(color_attrs)
        if app.config['DEBUG'] or app.config['TESTING']:
            query = """
                    INSERT INTO Colors (color_value) VALUES (?);
                    """
            DBMan.execute_sql_query(app, query, (color.color_value))

        else:
            db.session.add(color)
            db.session.commit()
        return color

    @staticmethod
    def update(color: ColorModel, updates: ColorInterface, app: Flask, db: SQLAlchemy) -> ColorModel:
        '''
        This method will update the current color in the database with its current values.
        If the color does not exist in the database it will save it.
        '''
        if not ColorService.retrieve_by_color_id(color.color_id):
            return ColorService.create(updates, app, db)
        else:
            color.update(updates)
            if app.config['DEBUG'] or app.config['TESTING']:
                query = """
                        UPDATE Colors
                        SET color_value = ?
                        WHERE color_id = ?;
                        """
                DBMan.execute_sql_query(app, query, (
                    color.color_value,
                    color.color_id
                    )
                )
            else:
                db.session.commit()
            return color

    @staticmethod
    def delete(color_id: int, app: Flask, db: SQLAlchemy) -> int:
        '''
        This method will delete a color from the database only if it exists.
        '''
        color: ColorModel = ColorService.retrieve_by_color_id(color.color_id)
        if color:
            if app.config['DEBUG'] or app.config['TESTING']:

                query = 'DELETE FROM Colors WHERE color_id = ?;'
                DBMan.execute_sql_query(app, query, (color.color_id,))

            else:
                db.session.delete(color)
                db.session.commit()
            return color_id
        return None

    @staticmethod
    def retrieve_by_color_id(color_id: int, app: Flask) -> ColorModel:
        '''
        This method searches the database for a color with the given color id.
        If the color does not exist it will return None.
        '''
        if app.config['DEBUG'] or app.config['TESTING']:
            query = 'SELECT * FROM Colors WHERE color_id = ?;'

            rows = DBMan.execute_sql_query(query, (color_id,))
            for row in rows:
                color: ColorModel = ColorModel()
                color.update(dict(
                    color_id = row[0],
                    color_value = row[1]
                ))
                return color
        else:
            return ColorModel.query.filter_by(color_id = color_id).first()
        return None

    @staticmethod
    def retrieve_all(app: Flask) -> List[ColorModel]:
        '''
        This method retrieves all the colors present in the database.
        '''
    #endregion