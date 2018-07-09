from flask_restful import Api, Resource
from flask import Flask, request
from flask_jsonpify import jsonify
import requests
import json

# independent function that create a bridge between a nano node and a public route for RESTful access

HOST = "" # machine ip
PORT = 6060
URI = "http://[::1]:7076"

def sendRpcRequest(data):
    data = json.dumps(data)

    response = requests.post(URI, data=data)
    if not response.ok:
        return None
    resp_dict = json.loads(response.text)
    return resp_dict

class Bridge(Resource):
    def post(self):
        json_dict = request.get_json()
        return jsonify(sendRpcRequest(json_dict))

def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Bridge, "/")
    
    if __name__ == "__main__":
        app.run(host=HOST, port=PORT)

main()
