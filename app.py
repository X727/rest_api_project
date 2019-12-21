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
    return get_initial_representation()

@app.route('/testapi/v1.0/supported_jukeboxes/', methods=['GET'])
def get_jukeboxes():
    set_id =  flask.request.args.get("settingId")
    model=  flask.request.args.get("model")
    offset=  flask.request.args.get("offset")
    limit=  flask.request.args.get("limit")
    
    if limit is None:
        #if limit was not specified set default value
        limit = 5
    else:
        #otherwise check if it is integer and abort with 400 status if not
        try:
            limit = int(limit)
        except:
            flask.abort(400, "limit parameter not a valid integer value.")
        
    if offset is None:
        #if offset was not specified set default value
        offset = 0
    else:
        #otherwise check if it is integer and abort with 400 status if not
        try:
            offset = int(offset)
        except:
             flask.abort(400, "offset parameter not a valid integer value.")
             
    if set_id is None:
        return get_initial_representation()
    
    #get all jukeboxes based on model parameter value and convert to json
    if model is not None:
        r = requests.get(jukebox_base_url+"?model={}".format(model))
    else:
        r = requests.get(jukebox_base_url)
    jukes = r.json()
    
    # If no response return 404 code
    if len(jukes) > 0:
        #find all jukes based on settingId parameter and return paginated json
        queried_jukes = find_all_jukes(set_id, jukes)
            
        paginated_jukes = [queried_jukes[i:i+limit] for i in range(0, len(queried_jukes), limit)]
        
        if offset > len(paginated_jukes):
            offset = len(paginated_jukes)-1
            
        json_reply = json.dumps(paginated_jukes[offset])
        
        return flask.Response(json_reply, mimetype="application/json")
    else:
        flask.abort(404, "The query did not return any response.")

# Function to return an intital representation of the data. 
# Merges the values returned by settings api with jukeboxes api
# This shows all jukeboxes that are supported by a given settingId, 
# allowing the user to better understand the api
def get_initial_representation(model=None):
    #get all jukeboxes based on model parameter value and convert to json
    if model is not None:
        r = requests.get(jukebox_base_url+"?model={}".format(model))
    else:
        r = requests.get(jukebox_base_url)
    jukes = r.json()
    r = requests.get(settings_base_url)
    settings = r.json()["settings"][0:9]
    
    for setting in settings:
        supported_jukes = find_all_jukes(setting["id"], jukes)
        setting["supported_jukeboxes"]=supported_jukes
        
    json_reply=json.dumps(settings)
    return flask.Response(json_reply, mimetype="application/json")


#Helper function that finds all requirements for a specified settingId value
#Returns set of components required to have the specified setting
def find_requirements(setting_id):
    r = requests.get(settings_base_url)
    settings = r.json()
    setting = [x for x in settings["settings"] if x["id"]==setting_id ]
    requirements = setting[0]["requires"]
    return set(requirements)

#Helper function that finds all jukes that meet the requirement for a  specified settingId
#Returns list of jukes that meet the requirements for a setting
def find_all_jukes(set_id, jukes):
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
    return queried_jukes
    
if __name__ == '__main__':
    app.run(debug=False)
