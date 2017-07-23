"""Build out Mheshimiwa api entry points and routes."""
import collections
from flask import url_for, request
from flask_restplus import Resource,reqparse
from .app import api, app
from . import utils

constituency_arguments = reqparse.RequestParser()
constituency_arguments.add_argument('county', type=str, required=False)


@api.route('/v0.2/constituencies', endpoint='get_constituencies')
class ConstituenciesResource(Resource):
    """Constituencies Details and Resources."""

    @api.expect(constituency_arguments, validate=True)
    def get(self):
        """List of Kenyan Constituencies.
        
        Build a list of Kenyan Constituencies providing Constituency Name, \n
        County Name, Representative and his/her party.     \n   
        Available Optional Filter on county (?county='County Name').
        """
        args = constituency_arguments.parse_args(request)
        this_county = args.get('county')
        if this_county:
            constituencies = utils.fetch_all_county_constituencies(
                str(this_county))
            if not constituencies:
                msg = 'No constituency found for {0}, check format or ' \
                      'detail'.format(this_county)
                return {'error': msg}, 404
        else:
            constituencies = utils.fetch_all_constituencies()
        if constituencies:
            constituency_list = {
                c.constituency_number: collections.OrderedDict([
                    ('Number', c.constituency_number),
                    ('Constituency', c.constituency_name),
                    ('Representative', c.representative),
                    ('County', c.county),
                    ('Party', c.party),
                    ('uri', url_for('get_constituency',
                                    constituency=c.constituency_name,
                                    _external=True))
                ]) for c in constituencies}
            constituency_list['items count'] = str(len(constituency_list))
            return constituency_list


@api.route('/v0.2/constituencies/<constituency>', endpoint='get_constituency')
class ConstituencyResource(Resource):
    """Single Constituency Details and Resources."""

    def get(self, constituency):
        """Specific Constituency Details.

        Fetch details of a specific constituency, including Constituency 
        Name, County Name, \n  
        Representative and his/her party. \n  
        Required Parameter name is the constituency name.
        """
        constituency = utils.fetch_specific_constituency(constituency)
        if constituency:
            constituency_list = {
                c.constituency_number: collections.OrderedDict([
                    ('Number', c.constituency_number),
                    ('Constituency', c.constituency_name),
                    ('Representative', c.representative),
                    ('County', c.county),
                    ('Party', c.party),
                    ('uri', url_for('get_constituency',
                                    constituency=c.constituency_name,
                                    _external=True))
                ]) for c in constituency}
            return constituency_list
        else:
            msg = 'No such constituency found, check format or detail'
            return {'error': msg}, 404


@api.route('/v0.2/counties')
class CountiesResource(Resource):
    """Counties Details and Resources."""

    def get(self):
        """List of Kenyan Counties.

        Build a list of Kenyan Counties showing County Number, Name, \n 
        Capital, Area in square kms and elected senator. \n
        No parameters required.
        """
        counties = utils.fetch_all_counties()
        if counties:
            county_list = {
                'County No:' + str(c.county_number): collections.OrderedDict([
                    ('County Number', c.county_number),
                    ('County', c.county),
                    ('Capital', c.capital),
                    ('Area (Sq.Km)', str(c.area)),
                    ('Senator', c.representative),
                    ('constituencies uri', url_for('get_constituencies',
                                    county=c.county, _external=True))
                ]) for c in counties}
            return county_list


@api.route('/v0.2/counties/<county>', endpoint='get_county')
class CountyResource(Resource):
    """Single County Details and Resources."""

    def get(self, county):
        """Specific County Details.

        Fetch a Kenyan County showing County Number, Name, \n 
        Capital, Area in square kms and elected senator. \n
        Required Parameter name is the county name.
        """
        county = utils.fetch_specific_county(county)
        if county:
            county_list = {
                c.county_number: collections.OrderedDict([
                    ('County Number', c.county_number),
                    ('County', c.county),
                    ('Capital', c.capital),
                    ('Area (Sq.Km)', str(c.area)),
                    ('county uri', url_for('get_county', county=c.county,
                                    _external=True)),
                    ('county_constituencies uri', url_for('get_constituencies',
                                        county=c.county, _external=True))
                ]) for c in county}
            return county_list
        else:
            msg = 'No such county found, check format or detail'
            return {'error': msg}, 404
