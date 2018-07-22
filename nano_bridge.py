from flask_restful import Api, Resource
from flask import Flask, request
from flask_jsonpify import jsonify
import requests
import json

# independent code that create a bridge between a nano node and a public route for RESTful access

class Bridge(Resource):
    def post(self):
        json_dict = request.get_json()
        return jsonify(sendRpcRequest(json_dict))

def config(*args):
    with open('config.json') as json_data_file:
        configuration = json.load(json_data_file)

    config_dict = configuration
    for argument in args:
        config_dict = config_dict[argument]
    return config_dict

def defaultHost(api = config("ip-api")):
    try:
        host = requests.get(api, timeout = float(config("timeout")) ).text
    except:
        host = config("host")
    finally:
        return host

def sendRpcRequest(data):
    data = json.dumps(data)

    response = requests.post(config("uri"), data = data, timeout = float(config("timeout")) )
    if not response.ok:
        return None
    resp_dict = json.loads(response.text)
    return resp_dict

app = Flask(__name__)
api = Api(app)

api.add_resource(Bridge, "/")
    
if __name__ == "__main__":
    try:
        app.run(host = defaultHost(), port = config("port"))
    except:
        app.run(host = config("host"), port = config("port"))

