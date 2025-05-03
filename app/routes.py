import uuid
from flask import render_template, request, redirect, url_for, abort
from app import app, db
from app.models import Poll, PollDate
from datetime import datetime

def format_date_option(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%a %-d %b")
    except Exception:
        return date_str

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        event_title = request.form.get('event_title', '').strip()
        selected_dates = request.form.get('selected_dates', '')
        selected_dates_list = [d for d in selected_dates.split(',') if d]

        # Generate a unique slug
        slug = uuid.uuid4().hex[:8]
        while Poll.query.filter_by(slug=slug).first():
            slug = uuid.uuid4().hex[:8]

        # Save poll and dates
        poll = Poll(slug=slug, event_title=event_title)
        db.session.add(poll)
        db.session.flush()  # Get poll.id before commit

        for date_str in selected_dates_list:
            db.session.add(PollDate(poll_id=poll.id, date_option=date_str))

        db.session.commit()
        return redirect(url_for('poll_response', slug=slug))
    return render_template('create_poll.html')

@app.route('/poll/<slug>', methods=['GET', 'POST'])
def poll_response(slug):
    poll = Poll.query.filter_by(slug=slug).first_or_404()
    date_options = [d.date_option for d in poll.dates]
    if request.method == 'POST':
        # Handle response submission here (not implemented in this step)
        pass
    return render_template(
        'poll_response.html',
        poll=poll,
        date_options=date_options,
        format_date_option=format_date_option
    ) 