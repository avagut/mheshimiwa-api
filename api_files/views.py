import collections
from flask import url_for, request
from flask_restplus import Resource,reqparse
from .app import api, app
from . import utils

constituency_arguments = reqparse.RequestParser()
constituency_arguments.add_argument('county', type=str, required=False)

@app.route('/howto')
def index():
    """Home Page."""

    return 'home page'


@api.route('/v2.0/constituencies', endpoint='get_constituencies')
class ConstituenciesResource(Resource):
    @api.expect(constituency_arguments, validate=True)
    def get(self):
        """List of Kenyan Constituencies.
        
        Build a list of Kenyan Constituencies.
        Available Filter on county.
        """
        args = constituency_arguments.parse_args(request)
        this_county = args.get('county')
        if this_county:
            constituencies = utils.fetch_all_county_constituencies(this_county)
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
                    ('Party', c.party)
                ]) for c in constituencies}
            return constituency_list


@api.route('/v2.0/constituencies/<constituency>', endpoint='get_constituency')
class ConstituencyResource(Resource):
    def get(self, constituency):
        """Specific Constituency Details.
        
        Fetch details of a specific constituency. \n
        Parameter name is the constituency name.
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


@api.route('/v2.0/counties')
class CountiesResource(Resource):
    def get(self):
        """List of Kenyan Counties.

        Build a list of Kenyan Counties.
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


@api.route('/v2.0/counties/<county>', endpoint='get_county')
class CountyResource(Resource):
    def get(self, county):
        """Specific County Details.

        Fetch details of a specific constituency. \n
        Parameter name is the constituency name.
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
                    ('constituencies uri', url_for('get_constituencies',
                                        county=c.county, _external=True))
                ]) for c in county}
            return county_list
        else:
            msg = 'No such county found, check format or detail'
            return {'error': msg}, 404
