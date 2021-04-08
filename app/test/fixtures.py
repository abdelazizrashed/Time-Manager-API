import pytest

from app import create_app, create_tables, drop_tables, execute_sql_query


@pytest.fixture
def app_test():
    return create_app("test")

@pytest.fixture
def app_prod():
    return create_app("prod")

@pytest.fixture
def client_test(app_test):
    return app_test.test_client()

@pytest.fixture
def client_prod(app_prod):
    return app_prod.test_client()

def setup_sqlite_db(app, table_name: str):
    
    query = "DELETE FROM {};".format(table_name)
    execute_sql_query(app, query)
    drop_tables(app)
    create_tables(app)

@pytest.fixture
def db(app_prod):
    from app import db

    with app_prod.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()