import os

from app import create_app
from app.shared.db_man.service import db

db.create_all()
app = create_app(os.getenv("FLASK_ENV") or "prod")
