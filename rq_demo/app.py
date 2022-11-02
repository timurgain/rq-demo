from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-low-priority-tasks/')
def start_low_tasks():
    return '<h1>Low</h1>'


@app.route('/start-default-priority-tasks/')
def start_default_tasks():
    return '<h1>Default</h1>'


@app.route('/start-high-priority-tasks/')
def start_high_tasks():
    return '<h1>High</h1>'
