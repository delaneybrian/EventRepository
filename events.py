from eventbrite import get_events as get_eventbrite_events
from meetup import get_events as get_meetup_events

def get_events(keyword, lat, lng):
    meetup_events = get_meetup_events(keyword, lat, lng)
    eventbrite_events = get_eventbrite_events(keyword, lat, lng)

    all_relevant_events =  meetup_events + eventbrite_events

    if all_relevant_events:
        return all_relevant_events
    else:
        error_message = "no events found for search term: {0}".format(keyword)
        return {'status': 'error', 'status_message': error_message}


