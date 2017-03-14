from flask import jsonify, make_response, request, Blueprint, render_template
from models.event import Event
from helpers.event import EventSchema

event_api = Blueprint('event_api', __name__)

@event_api.route('/',methods=["get"])
def get_event():
    """Event all event in time range."""
    json_data = request.args or {}
    return make_response(jsonify({ "data" : Event.get_events(json_data)}))

@event_api.route('/', methods=["post"])
def create_event():
    """Create new Calendar Event."""
    json_data = request.get_json()
    data, error = EventSchema().load(json_data)
    if error:
        return make_response(jsonify({"error": error}), 400)
    oEvent = Event.create(data)
    return make_response(jsonify(oEvent.as_dict()))

@event_api.route('/<int:id>',methods=["post"])
def update_event(id):
    """Update Event if Present else promt error."""
    import dateutil
    oEvent, error = Event.get_by_id(id)
    if error:
        return make_response(jsonify({"error" : error }), 400)
    json_data = request.get_json()
    # json_data['start_time'] = dateutil.parser.parse(json_data['start_time'])
    # json_data['end_time'] = dateutil.parser.parse(json_data['end_time'])
    # print json_data['start_time']
    data, error = EventSchema().load(json_data)
    if error:
        return make_response(jsonify({"error": error}), 400)
    oEvent = oEvent.update(data)
    return make_response(jsonify(oEvent.as_dict()))

@event_api.route('/<int:id>', methods=["delete"])
def delete_event(id):
    """Delete Event if Present."""
    oEvent, error = Event.get_by_id(id)
    if error:
        return make_response(jsonify({"error": error}), 400)
    oEvent.delete()
    return make_response(jsonify({"success": "Event Deleted"}))

@event_api.route('/<int:id>',methods=["get"])
def get_event_by_id(id):
    """Get Event."""
    oEvent, error = Event.get_by_id(id)
    print oEvent
    if error:
        return make_response(jsonify({"error": error}), 400)
    return make_response(jsonify(oEvent.as_dict()))
