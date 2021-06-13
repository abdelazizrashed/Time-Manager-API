from .user_model_interface import UserModelInterface
from app.shared.db_man.service import DBMan, db


class UserModel(db.Model):
    """
    The user model that is responsible for storing the user data.
    """

    __tablename__ = "Users"

    # region sqlalchemy table columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    is_admin = db.Column(db.Integer)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)
    # endregion

    def update(self, changes: UserModelInterface):
        for key, value in changes.items():
            setattr(self, key, value)
        return self
