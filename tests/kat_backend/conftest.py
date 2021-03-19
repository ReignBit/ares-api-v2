import pytest
from app.__main__ import create_app, db


@pytest.fixture
def client():
    # Change default testing database uri's to the dynamically created ones.

    flask = create_app('app.config.TestingConfig')
    db.init_app(flask)
    with flask.test_client() as client:
        with flask.app_context():
            db.create_all()
        yield client
