from models import RSVP

def generate_analytics(events):
    # Simple example: Count attendees per event
    analytics_data = []
    for event in events:
        rsvp_count = RSVP.query.filter_by(event_id=event.id).count()
        analytics_data.append({'event': event.name, 'attendees': rsvp_count})
    return analytics_data
