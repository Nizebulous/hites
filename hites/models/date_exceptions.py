from hites import db

from hites.models.pairings import Pairing


class DateException(db.Model):
    __tablename__ = 'date_exceptions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    pairing_id = db.Column(db.Integer, db.ForeignKey(Pairing.id))
    pairing = db.relationship(Pairing)
