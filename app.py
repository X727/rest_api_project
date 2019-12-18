# -*- coding: utf-8 -*-
"""
@author: patrick_ignoto
"""

import requests
import flask
import json

app = flask.Flask(__name__)
jukebox_base_url="http://my-json-server.typicode.com/touchtunes/tech-assignment/jukes"
settings_base_url="http://my-json-server.typicode.com/touchtunes/tech-assignment/settings"

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/test/api/v1.0/jukeboxes/', methods=['GET'])
def get_jukeboxes():
    set_id =  flask.request.args.get("settingId")
    model=  flask.request.args.get("model")
    offset=  flask.request.args.get("offset")
    limit=  flask.request.args.get("limit")
    
    if model is not None:
        r = requests.get(jukebox_base_url+"?model={}".format(model))
    else:
        r = requests.get(jukebox_base_url)
        
    if limit is None:
        limit = 5
    else:
        limit = int(limit)
        
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
    jukes = r.json()
    
    queried_jukes = []
    component_requirements = find_requirements(set_id)
    
    for juke in jukes:
        components = juke["components"]
        if len(components)==0:
            if len(component_requirements) == 0:
                queried_jukes.append(juke)
        else:
            component_names =set( [x["name"] for x in components])
            if component_requirements.issubset(component_names):
                queried_jukes.append(juke)

    
    paginated_jukes = [queried_jukes[i:i+limit] for i in range(0, len(queried_jukes), limit)]
    
    if offset > len(paginated_jukes):
        offset = len(paginated_jukes)-1
        
    json_reply = json.dumps(paginated_jukes[offset])
    
    return flask.Response(json_reply, mimetype="application/json")
    
def find_requirements(setting_id):
    r = requests.get(settings_base_url)
    settings = r.json()
    setting = [x for x in settings["settings"] if x["id"]==setting_id ]
    requirements = setting[0]["requires"]
    return set(requirements)

    
    
if __name__ == '__main__':
    app.run(debug=False)
