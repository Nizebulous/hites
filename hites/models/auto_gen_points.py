from hites import db

from hites.models.pairings import Pairing


class AutoGenPoint(db.Model):
    __tablename__ = 'auto_gen_points'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    point_type = db.Column(db.String(8))
    pairing_id = db.Column(db.Integer, db.ForeignKey(Pairing.id))
    pairing = db.relationship(Pairing)
