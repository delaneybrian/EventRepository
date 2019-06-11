from eventbrite import get_events as get_eventbrite_events
from meetup import get_events as get_meetup_events

def get_events(keyword, lat, lng):
    meetup_events = get_meetup_events(keyword, lat, lng)
    eventbrite_events = get_eventbrite_events(keyword, lat, lng)

    return meetup_events + eventbrite_events


