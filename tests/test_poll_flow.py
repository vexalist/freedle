import pytest
from app import app, db
from app.models import Poll

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_poll(client):
    response = client.post('/create', data={
        'event_title': 'Poker Night',
        'selected_dates': '2025-04-08,2025-04-10'
    }, follow_redirects=True)
    assert b'Poker Night' in response.data
    assert b'2025-04-08' in response.data

def test_submit_response(client):
    # Create poll first
    client.post('/create', data={
        'event_title': 'Test Event',
        'selected_dates': '2025-04-08,2025-04-10'
    })
    poll = Poll.query.first()
    response = client.post(f'/poll/{poll.slug}', data={
        'name': 'Alice',
        'dates': ['2025-04-08']
    }, follow_redirects=True)
    assert b'Alice' in response.data
    assert b'&#10003;' in response.data  # Checkmark as HTML entity

def test_duplicate_name(client):
    client.post('/create', data={
        'event_title': 'Test Event',
        'selected_dates': '2025-04-08'
    })
    poll = Poll.query.first()
    client.post(f'/poll/{poll.slug}', data={'name': 'Bob', 'dates': ['2025-04-08']})
    response = client.post(f'/poll/{poll.slug}', data={'name': 'Bob', 'dates': ['2025-04-08']})
    assert b'already submitted with that name' in response.data 