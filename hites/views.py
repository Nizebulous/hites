from datetime import date
from flask import jsonify
from datetime import timedelta
from calendar import monthrange
from flask import make_response
from flask import render_template

from hites import app
from hites.models.pairings import Pairing
from hites.models.auto_gen_points import AutoGenPoint
from hites.models.date_exceptions import DateException


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
    gen_point = AutoGenPoint.query.filter(
        AutoGenPoint.date < first_day
    ).order_by(AutoGenPoint.date.desc()).first()
    if gen_point and gen_point.point_type == 'start':
        anchor = gen_point.date
        anchor_index = gen_point.pairing_id - 1
    elif not gen_point or gen_point.point_type == 'stop':
        anchor = None
        anchor_index = None
    else:
        raise Exception('Invalid point type')
    additional_gen_points = {
        point.date.day: point for point in AutoGenPoint.query.filter(
            AutoGenPoint.date >= first_day
        ).filter(
            AutoGenPoint.date <= last_day
        ).all()

    }
    date_exceptions = {
        ex.date.day: ex.pairing for ex in DateException.query.filter(
            DateException.date >= first_day
        ).filter(
            DateException.date <= last_day
        ).all()
    }
    pairings = [pairing for pairing in Pairing.query.order_by(Pairing.id).all()]
    dates = {}
    index_date = first_day
    while (index_date.month == month):
        if index_date.day in date_exceptions:
            pairing = date_exceptions[index_date.day]
            if pairing:
                dates[index_date.day] = 'MODIFIED: %s & %s' % (
                    pairing.participant_one.name,
                    pairing.participant_two.name
                )
        else:
            if index_date.weekday() == 2 and anchor:  # Wednesday & not stopped
                pairing = pairings[
                    (
                        (
                            ((index_date - anchor).days) / 7  # number of weeks
                        ) % len(pairings)  # index into pairings array
                    ) + anchor_index  # offset for the starting paring
                ]
                dates[index_date.day] = '%s & %s' % (
                    pairing.participant_one.name,
                    pairing.participant_two.name
                )
        index_date += timedelta(days=1)
        if index_date.day in additional_gen_points:
            point = additional_gen_points[index_date.day]
            if point.point_type == 'start':
                anchor = point.date
                anchor_index = point.pairing_id - 1
            elif point.point_type == 'stop':
                anchor = None
                anchor_index = None
            else:
                raise Exception('Invalid point type')
    return jsonify(dates)


@app.route('/whose_turn')
def whose_turn():
    return render_template('calendar.html')
