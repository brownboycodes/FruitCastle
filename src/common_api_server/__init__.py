import sys, os
sys.path.append(os.path.abspath(os.path.join('.', 'src')))

import json
from flask import Flask, config, jsonify, send_from_directory, make_response, render_template

app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')

app.config.from_object('config.app_config.DevConfig')


@app.route('/')
def hello():
   
    return send_from_directory(app.template_folder, "index.html")

    # return render_template("index.html")


@app.route("/paypal-concept-data")
def paypal_concept_data():

    return render_template("dashboard.html",py_sent_data="someDoc")

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

@app.route('/paypal-concept-data/v1/docs')
def paypal_concept_data_v1_docs():
    return send_from_directory("paypal_concept_data/v1", "README.md")

@app.errorhandler(404)
def page_not_found(e):
    return make_response(
        render_template("error_page.html",error_code="404"),
        404
    )

@app.errorhandler(400)
def page_not_found(e):
    return make_response(
        render_template("error_page.html",error_code="400"),
        400
    )

@app.errorhandler(500)
def page_not_found(e):
    return make_response(
        render_template("error_page.html",error_code="500"),
        500
    )    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
