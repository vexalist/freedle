from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create')
def create_poll():
    return render_template('create_poll.html') 