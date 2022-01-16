from flask import Flask, config, jsonify, send_from_directory, make_response, render_template
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join('.', 'src')))


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')

app.config.from_object('config.app_config.DevConfig')


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/paypal-concept-data")
def paypal_concept_data():
    return render_template("dashboard.html", py_sent_data="PayPal concept data")


@app.route("/paypal-concept-data/v1")
def paypal_concept_data_v1():
    response_for_route = {
        "error": "please mention exactly what you want from version 1 of the paypal-concept-data API"}
    return jsonify(response_for_route)




def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


@app.route("/paypal-concept-data/v1/all-data")
def paypal_concept_data_v1_all_data():
    retrieved_file_data = get_json_data("src/data/users.json")
    return jsonify(retrieved_file_data)


@app.route("/paypal-concept-data/v1/all-users")
def paypal_concept_data_v1_all_users():
    retrieved_file_data = get_json_data("src/data/local_test_user_data.json")
    return jsonify(retrieved_file_data)


@app.route("/paypal-concept-data/v1/all-transactions")
def paypal_concept_data_v1_all_transactions():
    retrieved_file_data = get_json_data("src/data/transactions.json")
    return jsonify(retrieved_file_data)


@app.route("/paypal-concept-data/v1/all-contacts")
def paypal_concept_data_v1_all_contacts():
    retrieved_file_data = get_json_data("src/data/local_contacts.json")
    return jsonify(retrieved_file_data)


@app.route('/paypal-concept-data/v1/docs')
def paypal_concept_data_v1_docs():
    return send_from_directory("../docs/paypal_concept_data/v1", "paypal_concept_data_v1_wiki.md")


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
