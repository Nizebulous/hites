from hites import app
from flask import make_response
from flask import render_template


@app.route('/')
def index():
    return make_response('Hello World!!')


turns = [
    'Natalia & Zafirah',
    'Natalia & Kalil',
    'Zafirah & Ilori',
    'Zafirah & Kalil',
    'Ilori & Natalia',
    'Ilori & Kalil'
]


@app.route('/whose_turn')
def whose_turn():
    return render_template('calendar.html')
