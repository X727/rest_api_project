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
    return "test {} {} {} {}".format(set_id, model, offset, limit)
    
def find_requirements(setting_id):
    r = requests.get(settings_base_url)
    settings = r.json()
    setting = [x for x in settings["settings"] if x["id"]==setting_id ]
    requirements = setting[0]["requires"]
    return requirements
    
    
if __name__ == '__main__':
    app.run(debug=False)
