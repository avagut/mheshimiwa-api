from .app import api, db, app
from .models import Constituency, County, Representative
from sqlalchemy import func


def fetch_all_constituencies():
    """Get complete list of constituencies."""
    constituency_list = db.session.query(Constituency.constituency_number,
                                         Constituency.constituency_name,
                                         Constituency.county,
                                         Representative.representative,
                                         Representative.party) \
        .join(Representative, Constituency.constituency_name ==
              Representative.constituency).all()
    return constituency_list


def fetch_all_county_constituencies(county_name):
    """Get complete list of constituencies in a county."""
    selected_county_name = county_name.replace("+", " ")
    constituency_list = db.session.query(Constituency.constituency_number,
                                         Constituency.constituency_name,
                                         Constituency.county,
                                         Representative.representative,
                                         Representative.party) \
        .join(Representative, Constituency.constituency_name ==
              Representative.constituency) \
        .filter(func.lower(Constituency.county) ==
                func.lower(selected_county_name)).all()
    return constituency_list


def fetch_specific_constituency(constituency):
    """Fetch the details of select constituency"""
    selected_const = constituency.replace("+", " ")
    constituency = db.session.query(Constituency.constituency_number,
                                         Constituency.constituency_name,
                                         Constituency.county,
                                         Representative.representative,
                                         Representative.party) \
        .join(Representative, Constituency.constituency_name ==
              Representative.constituency) \
        .filter(func.lower(Constituency.constituency_name) ==
                func.lower(selected_const)).all()
    return constituency


def fetch_specific_county(county_name):
    """Fetch the details of select constituency"""
    selected_county_name = county_name.replace("+", " ")
    county = db.session.query(County.county_number, \
                             County.county, \
                             County.capital, \
                             County.area, \
                             Representative.representative, \
                             Representative.party) \
        .join(Representative, County.county == Representative.county) \
        .filter(Representative.is_senate == bool(1)) \
        .filter(func.lower(County.county)== func.lower(selected_county_name)) \
        .order_by(County.order_col).all()
    return county


def fetch_all_counties():
    """Get complete list of counties"""
    county_list = db.session.query(County.county_number, \
                             County.county, \
                             County.capital, \
                             County.area, \
                             Representative.representative, \
                             Representative.party) \
        .join(Representative, County.county == Representative.county) \
        .filter(Representative.is_senate == bool(1))\
        .order_by(County.order_col).all()
    return county_list


def validate_this_county(this_county):
    """Validate provided county name."""
    county = fetch_specific_county(this_county)
    if not county:
        return None
    else:
        county = county[0]
    constituencies = Constituency.query.filter(func.lower(
        Constituency.county) == func.lower(county.county)).all()
    return constituencies