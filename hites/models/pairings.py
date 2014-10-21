from hites import db

from hites.models.participants import Participant


class Pairing(db.Model):
    __tablename__ = 'pairings'
    id = db.Column(db.Integer, primary_key=True)
    participant_one_id = db.Column(db.Integer, db.ForeignKey(Participant.id))
    participant_one = db.relationship(Participant, foreign_keys='Pairing.participant_one_id')
    participant_two_id = db.Column(db.Integer, db.ForeignKey(Participant.id))
    participant_two = db.relationship(Participant, foreign_keys='Pairing.participant_two_id')
