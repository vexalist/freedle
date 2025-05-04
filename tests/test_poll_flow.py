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
    assert b'2025-04-10' in response.data
    # Should land on poll response page
    assert b'When could you be available?' in response.data

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
    # Check for SVG icon for available
    assert b'/static/icons/available.svg' in response.data
    # Tally column should appear
    assert b'Tally' in response.data

def test_duplicate_name(client):
    client.post('/create', data={
        'event_title': 'Test Event',
        'selected_dates': '2025-04-08'
    })
    poll = Poll.query.first()
    client.post(f'/poll/{poll.slug}', data={'name': 'Bob', 'dates': ['2025-04-08']})
    response = client.post(f'/poll/{poll.slug}', data={'name': 'Bob', 'dates': ['2025-04-08']})
    assert b'already submitted with that name' in response.data

def test_name_required(client):
    client.post('/create', data={
        'event_title': 'Test Event',
        'selected_dates': '2025-04-08'
    })
    poll = Poll.query.first()
    response = client.post(f'/poll/{poll.slug}', data={'name': '', 'dates': ['2025-04-08']})
    assert b'Name is required' in response.data

def test_date_required(client):
    client.post('/create', data={
        'event_title': 'Test Event',
        'selected_dates': '2025-04-08,2025-04-09'
    })
    poll = Poll.query.first()
    response = client.post(f'/poll/{poll.slug}', data={'name': 'Eve', 'dates': []})
    assert b'Please select at least one date' in response.data

def test_tally_column_hidden_when_no_participants(client):
    # Create poll
    response = client.post('/create', data={
        'event_title': 'No Participants Event',
        'selected_dates': '2025-05-01,2025-05-02'
    }, follow_redirects=True)
    # On the response page, tally column should NOT appear
    assert b'Tally' not in response.data
    # Should still show date options
    assert b'2025-05-01' in response.data
    assert b'2025-05-02' in response.data

def test_tally_column_shown_when_participants_exist(client):
    # Create poll
    client.post('/create', data={
        'event_title': 'With Participants Event',
        'selected_dates': '2025-06-01,2025-06-02'
    })
    poll = Poll.query.first()
    # Submit a response
    client.post(f'/poll/{poll.slug}', data={
        'name': 'Charlie',
        'dates': ['2025-06-01']
    }, follow_redirects=True)
    # Reload response page
    response = client.get(f'/poll/{poll.slug}')
    # Tally column should appear
    assert b'Tally' in response.data
    assert b'Charlie' in response.data

def test_end_to_end_tally_column_flow(client):
    # User creates a poll
    response = client.post('/create', data={
        'event_title': 'End to End Event',
        'selected_dates': '2025-07-01,2025-07-02'
    }, follow_redirects=True)
    # No participants yet, tally column should not be present
    assert b'Tally' not in response.data
    # User submits a response
    poll = Poll.query.first()
    response = client.post(f'/poll/{poll.slug}', data={
        'name': 'Dana',
        'dates': ['2025-07-01', '2025-07-02']
    }, follow_redirects=True)
    # Tally column should now be present
    assert b'Tally' in response.data
    assert b'Dana' in response.data
    # Check for available SVG icon
    assert b'/static/icons/available.svg' in response.data 