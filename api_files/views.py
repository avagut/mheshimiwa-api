import collections
from flask_restplus import Resource
from sqlalchemy import func
from .app import api, db
from .models import Constituency


@api.route('/v2.0/constituencies')
class ConstituenciesResource(Resource):
    def get(self):
        """List of Kenyan Constituencies.

        Build a list of Kenyan Constituencies.
        No parameters required.
        """
        constituencies = db.session.query(Constituency).all()
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


@api.route('/v2.0/constituencies/<constituency>')
class ConstituencyResource(Resource):
    def get(self, constituency):
        """Specific Constituency Details.
        
        Fetch details of a specific constituency. \n
        Parameter name is the constituency name.
        """
        selected_const = constituency.replace("+", " ")
        constituency = Constituency.query.filter(func.lower(
            Constituency.constituency_name) == func.lower(selected_const)
                                                 ).all()
        if constituency:
            constituency_list = {
                c.constituency_number: collections.OrderedDict([
                    ('Number', c.constituency_number),
                    ('Constituency', c.constituency_name),
                    ('Representative', c.representative),
                    ('County', c.county),
                    ('Party', c.party)
                ]) for c in constituency}
            return constituency_list
        else:
            msg = 'No such constituency found, check format or detail'
            return {'error': msg}, 404
