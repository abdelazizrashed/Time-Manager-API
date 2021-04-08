from app.shared.db_man.service import DBMan

db = DBMan.get_db()

class TokenBlocklistModel(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    jti = db.Column(
        db.String(36),
        nullable = False
    )
    created_at = db.Column(
        db.DateTime,
        nullable = False
    )