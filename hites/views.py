from datetime import date
from flask import jsonify
from datetime import timedelta
from calendar import monthrange
from flask import make_response
from flask import render_template

from hites import app
from hites.packages.woodworking import WoodWorkingEventBank


@app.route('/')
def index():
    return make_response('Hello World!!')


@app.route('/status')
def status():
    import os
    return jsonify({'environment': dict(os.environ)})


@app.route('/woodworking/<int:year>/<int:month>/events')
def woodworking_month_events(year, month):
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    ww_events = WoodWorkingEventBank(first_day, last_day)
    dates = {}
    index_date = first_day
    while (index_date.month == month):
        if index_date in ww_events:
            dates[index_date.day] = ww_events[index_date]
        index_date += timedelta(days=1)
    return jsonify(dates)


@app.route('/whose_turn')
def whose_turn():
    return render_template('calendar.html')
