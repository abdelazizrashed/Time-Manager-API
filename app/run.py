from app import app
from db_man import DBMan
from config_module import ProductionConfig


DBMan.db.init_app(app)

app.config.from_object(ProductionConfig)

@app.before_first_request
def create_tables():
    DBMan.db.create_all()
