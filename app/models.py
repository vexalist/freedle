from app import db
from datetime import datetime

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(32), unique=True, nullable=False)
    event_title = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    dates = db.relationship('PollDate', backref='poll', cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='poll', cascade='all, delete-orphan')

class PollDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    date_option = db.Column(db.String(16), nullable=False)
    responses = db.relationship('ResponseSelection', backref='poll_date', cascade='all, delete-orphan')

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    selections = db.relationship('ResponseSelection', backref='response', cascade='all, delete-orphan')

class ResponseSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('response.id'), nullable=False)
    poll_date_id = db.Column(db.Integer, db.ForeignKey('poll_date.id'), nullable=False) 