#
#
# Module to find relevant events from meetup and return in a standard format
#
#

import requests
import json
import logging
import traceback
import datetime

client_id = 'a4t8djnuofg711ol9n123d5kqr'
client_secret = '621ss2n05shh4jj8n5ede6oh92'
refresh_token = '14c958013bee8d48b911f78389d7d1dd'


def get_events(keyword, lat, lng):
    """Get events from the meetup api relevant to the given arguments

    :param keyword: a keyword to filter events on e.g. python
    :param lat: a latitude coordinate relevant to the user
    :param lng: a longitude coordinate relevant to the user
    :return: a list of json events relevant to the location and keyword or an error message if error encountered
    """
    radius = 30
    relevant_events = []
    try:
        event_results = get_meetup_events(lat, lng, radius, keyword)
        internal_events = convert_external_events_to_internal(event_results)
        relevant_events = filter_events_on_keyword(keyword, internal_events)
    except Exception as error:
        print('Error occurred: {0}'.format(error))
        logging.error(traceback.format_exc())

    return relevant_events


def get_new_access_token():
    refresh_url = 'https://secure.meetup.com/oauth2/access?client_id={0}&client_secret={1}&grant_type=refresh_token&refresh_token={2}'.format(client_id, client_secret, refresh_token)
    r = requests.post(refresh_url)
    content = json.loads(r.content.decode('utf-8'))
    return(content["access_token"])


def get_meetup_events(lat, lng, radius, keyword):
    tech_cat_id = 34
    access_token = get_new_access_token()
    headers = {'Authorization': 'Bearer {0}'.format(access_token)}
    events_url = 'https://api.meetup.com/find/upcoming_events?lat={0}&lon={1}&radius={2}&topic_category={3}&text={4}'.format(
        lat, lng, radius, tech_cat_id, keyword)

    r = requests.get(events_url, headers=headers)
    content = json.loads(r.content.decode('utf-8'))
    return content['events']


def calculate_event_start_time(local_time, utc_offset):
    ticks = local_time + utc_offset
    return datetime.datetime.utcfromtimestamp(ticks / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')


def calculate_event_end_time(local_time, utc_offset, duration):
    ticks = local_time + utc_offset + duration
    return datetime.datetime.utcfromtimestamp(ticks / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')


def convert_external_events_to_internal(event_results):
    internal_events = []

    for event in event_results:

        try:
            if ('name' in event.keys()):
                name = event['name']
            else:
                name = ''

            if ('description' in event.keys()):
                description = event['description']
            else:
                description = ''

            if ('time' in event.keys()):
                time = event['time']
            else:
                time = 0

            if ('duration' in event.keys()):
                duration = event['duration']
            else:
                duration = 0

            if ('utc_offset' in event.keys()):
                utc_offset = event['utc_offset']
            else:
                utc_offset = 0

            if ('id' in event.keys()):
                id = event['id']
            else:
                id = ''

            if ('link' in event.keys()):
                url = event['link']
            else:
                url = ''

            if ('group' in event.keys()):
                group = event['group']
                if ('name' in group.keys()):
                    summary = group['name']
                else:
                    summary = ""
            else:
                summary = ""

            if ('venue' in event.keys()):
                venue = event['venue']
                if ('name' in venue.keys()):
                    address_line_1 = venue['name']
                else:
                    address_line_1 = ""
                if ('address_1' in venue.keys()):
                    address_line_2 = venue['address_1']
                else:
                    address_line_2 = ""
                if ('city' in venue.keys()):
                    city = venue['city']
                else:
                    city = ""
                if ('country' in venue.keys()):
                    country = venue['country']
                else:
                    country = ""
                if ('lat' in venue.keys()):
                    lat = venue['lat']
                else:
                    lat = 0
                if ('lon' in venue.keys()):
                    lng = venue['lon']
                else:
                    lng = 0
            else:
                address_line_1 = ""
                address_line_2 = ""
                lat = 0
                lng = 0
                city = ""
                country = ""

            internal_event = {
                'name': name,
                'description': description,
                'start_time_utc': calculate_event_start_time(time, utc_offset),
                'end_time_utc': calculate_event_end_time(time, utc_offset, duration),
                'id': id,
                'is_free': 'True',
                'url': url,
                'summary': summary,
                'address_line_1': address_line_1,
                'address_line_2': address_line_2,
                'city': city,
                'country': country,
                'lat': lat,
                'lng': lng,
                'source': 'meetup'
            }

            internal_events.append(internal_event)
        except Exception as error:
            print('Error occurred in parsing: {0}'.format(error))
            logging.error(traceback.format_exc())

    return internal_events


def filter_events_on_keyword(keyword, internal_events):
    """Filter events on a keyword, filters based on name, summary and description of event

    :param keyword: the keyword to filter the internal events on
    :param internal_events: the events we wish to filter
    :return: list of filtered internal events
    """
    relevant_events = []

    for internal_event in internal_events:
        is_relevant = event_contains_keyword(keyword, internal_event)

        if (is_relevant):
            relevant_events.append(internal_event)

    return relevant_events


def event_contains_keyword(keyword, event):
    normalized_keyword = keyword.upper()

    normalized_name = event['name'].upper()
    normalized_description = event['description'].upper()
    normalized_summary = event['summary'].upper()

    if normalized_keyword in normalized_name:
        return True

    if normalized_keyword in normalized_description:
        return True

    if normalized_keyword in normalized_summary:
        return True

    return False
