import os

from app import create_app
from app.shared.db_man.service import db

app = create_app(os.getenv("FLASK_ENV") or "prod")

with app.app_context():
    db.create_all()
