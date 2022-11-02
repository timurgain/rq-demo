from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    print('Такие дела')
    return '<h1>Hello, TM</h1>'
