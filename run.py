import os

from app import create_app
from app.shared.db_man.service import db


if __name__ == "__main__":
    db.create_all()