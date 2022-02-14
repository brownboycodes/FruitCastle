from flask import Flask, jsonify, make_response, render_template
import json

from flask_cors import CORS
from .paypal_concept_data.paypal_concept_data import paypal_concept_data


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')
app.register_blueprint(paypal_concept_data)
CORS(app)


def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about/brownboycodes')
def about_brownboycodes():
    retrieved_file_data = get_json_data(
        "src/data/brownboycodes.json")
    return jsonify(retrieved_file_data)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(
        render_template("error_page.html", error_code="404"),
        404
    )


@app.errorhandler(400)
def page_not_found(e):
    return make_response(
        render_template("error_page.html", error_code="400"),
        400
    )


@app.errorhandler(500)
def page_not_found(e):
    return make_response(
        render_template("error_page.html", error_code="500"),
        500
    )
