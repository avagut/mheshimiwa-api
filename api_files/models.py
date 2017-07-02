"""Capture Data Details"""

from .app import db


class Constituency(db.Model):
    """Constituency Details."""
    __tablename__ = 'constituencies'
    cons_id = db.Column(db.Integer, primary_key=True)
    constituency_number = db.Column(db.String(250), nullable=False,
                                    unique=True)
    constituency_name = db.Column(db.String(250), nullable=False, unique=True)
    representative = db.Column(db.String(250), nullable=False, unique=True)
    county = db.Column(db.String(250), nullable=False)
    party = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False)
