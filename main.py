from events import get_events

lat = 53.350140
lng = -6.266155
events = get_events('java', lat, lng)

print(events)