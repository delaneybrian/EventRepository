#!/usr/bin/env python3
#
# UCD Abracadata - YouSights project Events microservice

# import python libs
from flask import request, jsonify, abort
from flask_restplus import Resource
import logging
# import modules
from __init__ import app, api
import json

#import event source
from events import get_events

# import API models
from api_models import event_list_response_model, event_query_model

logging.getLogger(__name__)


# Youtube mockup API
@api.route('/events')
class YouSightsEvents(Resource):
    @api.doc(description="Events API to get list of events from various sources including meetup and eventbrite")
    @api.expect(event_query_model)
    def post(self):
        request_info = request.json
        search_topic = request_info['keyword']
        search_lng = request_info['lng']
        search_lat = request_info['lat']
        events = get_events(search_topic, search_lat, search_lng)
        if events:
            print(events)
            return json.dumps(events)
        else:
            abort(404, events)
        return jsonify(error="error while processing data")

# start server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)