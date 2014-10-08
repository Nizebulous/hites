from hites import app
from flask import make_response

from datetime import date
from datetime import timedelta


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
    start_date = date(2014, 9, 3)
    today = date.today()
    next_wednesday = today + timedelta(days=(2 - today.weekday()) % 7)
    date_diff = next_wednesday - start_date
    week_index = date_diff.days / 7
    output = 'On the next Wednesday(%s): %s' % (
        next_wednesday, turns[week_index % len(turns)]
    )
    return make_response(output)
