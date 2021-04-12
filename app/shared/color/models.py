from ..db_man.service import db
from .interfaces import ColorInterface


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

    def update(self, color_attrs: ColorInterface):

        for key, value in color_attrs.keys():
            setattr(self, key, value)

        return self