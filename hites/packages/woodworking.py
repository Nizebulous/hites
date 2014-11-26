from datetime import timedelta

from hites.models.pairings import Pairing
from hites.models.auto_gen_points import AutoGenPoint
from hites.models.date_exceptions import DateException


class WoodWorkingEventBank:

    def __init__(self, first_day, last_day):
        self.first_day = first_day
        self.last_day = last_day

    def __getitem__(self, date):
        event = ''
        if date in self._exception_dates:
            pairing = self._exception_dates[date]
            event += '*MODIFIED* '
        else:
            pairing = self._generated_dates[date]
        if pairing:
            event += '%s & %s' % (
                pairing.participant_one.name,
                pairing.participant_two.name
            )
        else:
            event = 'SKIPPED'
        return event

    def __contains__(self, date):
        return date in self._exception_dates or date in self._generated_dates

    @property
    def _pairings(self):
        if '_pairings' not in self.__dict__:
            self.__dict__['_pairings'] = [pairing for pairing in Pairing.query.order_by(Pairing.id).all()]
        return self.__dict__['_pairings']

    @property
    def _exception_dates(self):
        if '_exception_dates' not in self.__dict__:
            self.__dict__['_exception_dates'] = {
                ex.date: ex.pairing for ex in DateException.query.filter(
                    DateException.date >= self.first_day
                ).filter(
                    DateException.date <= self.last_day
                ).all()
            }
        return self.__dict__['_exception_dates']

    @property
    def _generated_dates(self):
        if '_generated_dates' not in self.__dict__:
            self.__dict__['_generated_dates'] = self._get_generated_dates()
        return self.__dict__['_generated_dates']

    def _get_generated_dates(self):
        # First Wednesday after the first day
        gen_date = self.first_day + timedelta(days=((2 - self.first_day.weekday()) % 7))

        generated_dates = {}
        # Need to load the first gen point (before first_day)
        gen_point = AutoGenPoint.query.filter(
            AutoGenPoint.date <= gen_date
        ).order_by(AutoGenPoint.date.desc()).first()
        additional_gen_points = [
            point for point in AutoGenPoint.query.filter(
                AutoGenPoint.date > gen_date
            ).filter(
                AutoGenPoint.date <= self.last_day
            ).all()
        ]

        gp_index = 0
        while gen_date <= self.last_day:
            if gen_point.point_type == 'start':
                pairing = self._pairings[
                    (
                        (
                            ((gen_date - gen_point.date).days) / 7  # number of weeks
                        ) + gen_point.pairing_id - 1  # offset for the starting paring
                    ) % len(self._pairings)  # index into pairings array
                ]
            else:
                pairing = None
            generated_dates[gen_date] = pairing
            next_date = gen_date + timedelta(days=7)
            while gp_index < len(additional_gen_points) and additional_gen_points[gp_index].date <= next_date:
                gen_point = additional_gen_points[gp_index]
                gp_index += 1
            gen_date = next_date
        return generated_dates
