import os
from dotenv import load_dotenv
import pytest
from app import create_app

@pytest.fixture
def client():
    load_dotenv()
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_db(client):
    db = client.config['DB']
    assert db.name.endswith('-test'), f"Expected test DB, got {db.name}"
    yield client.config['DB']
    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)

@pytest.fixture
def test_user_collection(test_db):
    return test_db['test_users']

@pytest.fixture
def test_flashcard_collection(test_db):
    return test_db['test_flashcards']
    
