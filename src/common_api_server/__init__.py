import json
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route("/paypal-concept-data")
def paypal_concept_data():
    response_for_route = {
        "error": "please mention the correct version of the paypal-concept-data API"}
    return jsonify(response_for_route)


@app.route("/paypal-concept-data/v1")
def paypal_concept_data_v1():
    response_for_route = {
        "error": "please mention exactly what you want from version 1 of the paypal-concept-data API"}
    return jsonify(response_for_route)


json_file = open("src/data/users.json", "r")
json_file_raw = json_file.read()
json_file_parsed = json.loads(json_file_raw)


@app.route("/paypal-concept-data/v1/all-data")
def paypal_concept_data_v1_all_data():
    return jsonify(json_file_parsed)
