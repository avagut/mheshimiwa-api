"""Capture Data Details"""

from .app import db

class Constituency(db.Model):
    """Constituency Details."""
    __tablename__ = 'constituencies'
    cons_id = db.Column(db.Integer, primary_key=True)
    constituency_number = db.Column(db.String(250), nullable=False,
                                    unique=True)
    constituency_name = db.Column(db.String(250), nullable=False, unique=True)
    county = db.Column(db.String(250), nullable=False)


class County(db.Model):
    """County Details"""
    __tablename__ = 'counties'
    county_id = db.Column(db.Integer, primary_key=True)
    county_number = db.Column(db.String(250), nullable=False, unique=True)
    county = db.Column(db.String(250), nullable=False, unique=True)
    capital = db.Column(db.String(250), nullable=False)
    area = db.Column(db.Numeric, nullable=False)
    order_col = db.Column(db.Numeric, nullable=False)


class Representative(db.Model):
    """Representative Details."""
    __tablename__ = 'representatives'
    representative_id = db.Column(db.Integer, primary_key=True)
    representative = db.Column(db.String(250), nullable=False)
    constituency = db.Column(db.String(250), nullable=True)
    county = db.Column(db.String(250), nullable=True)
    status = db.Column(db.String(250), nullable=False)
    parliament = db.Column(db.String(250), nullable=False)
    party = db.Column(db.String(250), nullable=False)
    is_senate = db.Column(db.Boolean, nullable=False)
    special_interest = db.Column(db.String(250), nullable=False)