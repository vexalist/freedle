import uuid
from flask import render_template, request, redirect, url_for, abort
from app import app, db
from app.models import Poll, PollDate, Response, ResponseSelection
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
    date_options = [d for d in poll.dates]
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        selected_dates = request.form.getlist('dates')
        if not name:
            error = 'Name is required.'
        elif not selected_dates:
            error = 'Please select at least one date.'
        elif Response.query.filter_by(poll_id=poll.id, name=name).first():
            error = 'Someone has already submitted with that name.'
        else:
            # Save response
            response = Response(poll_id=poll.id, name=name)
            db.session.add(response)
            db.session.flush()  # Get response.id
            for date_str in selected_dates:
                poll_date = PollDate.query.filter_by(poll_id=poll.id, date_option=date_str).first()
                if poll_date:
                    db.session.add(ResponseSelection(response_id=response.id, poll_date_id=poll_date.id))
            db.session.commit()
            return redirect(url_for('poll_results', slug=slug))

    # --- New: Prepare data for response grid ---
    participants = [r.name for r in poll.responses]
    date_labels = [format_date_option(d.date_option) for d in date_options]
    grid = []
    for d in date_options:
        row = []
        for r in poll.responses:
            selected = any(sel.poll_date_id == d.id for sel in r.selections)
            row.append(selected)
        grid.append(row)

    poll_url = request.url
    return render_template(
        'poll_response.html',
        poll=poll,
        date_options=date_options,
        error=error,
        poll_url=poll_url,
        format_date_option=format_date_option,
        participants=participants,
        date_labels=date_labels,
        grid=grid
    )

@app.route('/poll/<slug>/results')
def poll_results(slug):
    poll = Poll.query.filter_by(slug=slug).first_or_404()
    date_options = [d for d in poll.dates]
    participants = [r.name for r in poll.responses]
    date_labels = [format_date_option(d.date_option) for d in date_options]
    grid = []
    tallies = []
    for d in date_options:
        row = []
        count = 0
        for r in poll.responses:
            selected = any(sel.poll_date_id == d.id for sel in r.selections)
            row.append(selected)
            if selected:
                count += 1
        grid.append(row)
        tallies.append(count)
    poll_url = url_for('poll_response', slug=slug, _external=True)
    return render_template(
        'poll_results.html',
        poll=poll,
        date_options=date_options,
        date_labels=date_labels,
        participants=participants,
        grid=grid,
        poll_url=poll_url,
        format_date_option=format_date_option,
        tallies=tallies
    ) 