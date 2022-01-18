from datetime import datetime, timedelta, timezone
import random
import re
from urllib import response
from flask import Flask, config, jsonify, send_from_directory, make_response, render_template, request
import json
import sys
import os
import jwt
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join('.', 'src')))


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')

CORS(app)

# app.config.from_object('config.app_config.DevConfig')
# app.config.from_object('config.app_config.ProductionConfig')

male_image_filenames = next(os.walk(
    'src/common_api_server/client/dist/images/paypal_concept_images/paypal_concept_users/male'), (None, None, []))[2]

female_image_filenames = next(os.walk(
    'src/common_api_server/client/dist/images/paypal_concept_images/paypal_concept_users/female'), (None, None, []))[2]


valid_email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

secret_key_jwt = "3v9fIXKwsOn9bp4vI2amfLrSx3wJ2gF8STMtEJLjM5kPVXdWFoTPOiABiNhuGvLf0Y2hoaJm7LuCUTH5mKTayjm2338mzGgmpUUwN49IhrH9Kb4Htrb6TkPjWzeMz1RzKh8yhD2BmeuTrb2st2KQfisQs2eIs7LKQu37W68bfhVG0ryecIO0q7JK4Q1fewFHRP0RI2p0"

# token_expiration_date = datetime.now(tz=timezone.utc)+timedelta(minutes=3)


def decode_json_token(encoded_token):
    try:
        decoded_token = jwt.decode(
            encoded_token, secret_key_jwt, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {'error': "your session has expired please login again"}
    except jwt.InvalidTokenError:
        return {'error': 'suspicious activity detected'}


def json_token_validifier(encoded_token):
    try:
        decoded_token = jwt.decode(
            encoded_token, secret_key_jwt, algorithms=["HS256"])
        return "valid"
    except jwt.ExpiredSignatureError:
        return "invalid"
    except jwt.InvalidTokenError:
        return "invalid"


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


@app.route("/paypal-concept-data/v1/user/<int:user_id>", methods=['POST', 'GET'])
def paypal_concept_data_v1_get_user_by_id(user_id):
    login_response = {"error": "something went wrong"}
    if request.method == 'GET':
        login_response = {"error": "this is a GET request"}
    if request.method == 'POST':
        received_hash = request.json['hash']
        token_status = json_token_validifier(received_hash)
        if token_status == "valid":
            retrieved_file_data = get_json_data(
                "src/data/local_test_user_data.json")['users']
            filtered_data = [
                x for x in retrieved_file_data if x['id'] == user_id]
            if len(filtered_data) != 0:
                if filtered_data[0]['gender'] == "Female":
                    filtered_data[0]['avatar'] = random.choice(
                        female_image_filenames)
                else:
                    filtered_data[0]['avatar'] = random.choice(
                        male_image_filenames)
                login_response = {'users': filtered_data}
            else:
                login_response = {'error': "user not found"}
        else:
            login_response = {
                'error': "session is invalid, please login again"}
    return jsonify(login_response)


@app.route("/paypal-concept-data/v1/user/login", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_login():
    if request.method == 'POST':
        login_response = {'error': 'some error occurred'}
        username_or_email = request.json['userInput']
        entered_password = request.json['password']

        retrieved_file_data = get_json_data(
            "src/data/local_test_user_data.json")['users']
        if re.fullmatch(valid_email_regex, username_or_email):
            filtered_data = [
                x for x in retrieved_file_data if x['email'] == username_or_email]
            if len(filtered_data) != 0:
                if entered_password == filtered_data[0]['password']:
                    successful_hash = jwt.encode(
                        {'users': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=3)}, secret_key_jwt, algorithm="HS256")
                    login_response = {'hash': successful_hash}
                else:
                    login_response = {'error': "incorrect password"}
            else:
                login_response = {
                    'error': "no account found with the email address provided"}
        else:
            filtered_data = [
                x for x in retrieved_file_data if x['username'] == username_or_email]
            if len(filtered_data) != 0:
                if entered_password == filtered_data[0]['password']:
                    successful_hash = jwt.encode(
                        {'users': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=3)}, secret_key_jwt, algorithm="HS256")
                    login_response = {'hash': successful_hash}
                else:
                    login_response = {'error': "incorrect password"}
            else:
                login_response = {
                    'error': "no account found with the username provided"}
        return jsonify(login_response)

    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})


@app.route("/paypal-concept-data/v1/user/verify-login", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_verify_login():
    if request.method == 'POST':
        encoded_token = request.json['hash']
        decoded_token = decode_json_token(encoded_token)
        return jsonify(decoded_token)
    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})


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


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
