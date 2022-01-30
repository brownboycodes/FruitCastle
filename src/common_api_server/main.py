from datetime import datetime, timedelta, timezone
import random
import re
from uuid import uuid4

from flask import Flask, jsonify, send_from_directory, make_response, render_template, request
import json

import os
import jwt
from flask_cors import CORS


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')

CORS(app)


male_image_filenames = next(os.walk(
    'src/common_api_server/client/dist/images/paypal_concept_images/paypal_concept_users/male'), (None, None, []))[2]

female_image_filenames = next(os.walk(
    'src/common_api_server/client/dist/images/paypal_concept_images/paypal_concept_users/female'), (None, None, []))[2]


valid_email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

secret_key_jwt = "3v9fIXKwsOn9bp4vI2amfLrSx3wJ2gF8STMtEJLjM5kPVXdWFoTPOiABiNhuGvLf0Y2hoaJm7LuCUTH5mKTayjm2338mzGgmpUUwN49IhrH9Kb4Htrb6TkPjWzeMz1RzKh8yhD2BmeuTrb2st2KQfisQs2eIs7LKQu37W68bfhVG0ryecIO0q7JK4Q1fewFHRP0RI2p0"


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
        return decoded_token
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

# ? PURPOSE: for extracting json data from file


def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


@app.route("/paypal-concept-data/v1/all-data", methods=['POST', 'GET'])
def paypal_concept_data_v1_all_data():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data("src/data/users.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'error': "your session has expired please login again"})


@app.route("/paypal-concept-data/v1/all-users", methods=['POST', 'GET'])
def paypal_concept_data_v1_all_users():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/local_test_user_data.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'error': "your session has expired please login again"})

# ? PURPOSE: to allow an already logged in user to access their account if they have a valid token


@app.route("/paypal-concept-data/v1/user/<int:user_id>", methods=['POST', 'GET'])
def paypal_concept_data_v1_get_user_by_id(user_id):
    login_response = {"error": "something went wrong"}
    if request.method == 'GET':
        login_response = {"error": "this is a GET request"}
    if request.method == 'POST':
        received_hash = request.json['hash']
        token_status = json_token_validifier(received_hash)
        if token_status != "invalid":
            if token_status['userId'] == user_id:
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
                    login_response = {'user': filtered_data[0]}
                else:
                    login_response = {'error': "user not found"}
            else:
                login_response = {
                    'error': "access denied! suspicious login detected"}
        else:
            login_response = {
                'error': "session is invalid, please login again"}
    return jsonify(login_response)

# ? PURPOSE: to allow the user to access their account when they sign in from their device


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
                        {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=30)}, secret_key_jwt, algorithm="HS256")
                    if filtered_data[0]['gender'] == "Female":
                        filtered_data[0]['avatar'] = random.choice(
                            female_image_filenames)
                    else:
                        filtered_data[0]['avatar'] = random.choice(
                            male_image_filenames)
                    login_response = {
                        'hash': successful_hash, 'user': filtered_data[0]}
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
                        {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=30)}, secret_key_jwt, algorithm="HS256")
                    if filtered_data[0]['gender'] == "Female":
                        filtered_data[0]['avatar'] = random.choice(
                            female_image_filenames)
                    else:
                        filtered_data[0]['avatar'] = random.choice(
                            male_image_filenames)
                    login_response = {
                        'hash': successful_hash, 'user': filtered_data[0]}
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

# ? PURPOSE: for extracting transaction records


@app.route("/paypal-concept-data/v1/all-transactions", methods=['POST', 'GET'])
def paypal_concept_data_v1_all_transactions():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data("src/data/transactions.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'error': "your session has expired please login again"})

# ? PURPOSE: for extracting contacts of the user


@app.route("/paypal-concept-data/v1/all-contacts", methods=['POST', 'GET'])
def paypal_concept_data_v1_all_contacts():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data("src/data/local_contacts.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'error': "your session has expired please login again"})

# ? PURPOSE: for retrieving cards available for the user


@app.route("/paypal-concept-data/v1/available-cards", methods=['POST', 'GET'])
def paypal_concept_data_v1_available_cards():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data("src/data/card_data.json")
            available_cards = retrieved_file_data['availableCards']
            random.shuffle(available_cards)
            number_of_cards = random.choice(range(1, 5))
            return jsonify({'availableCards': available_cards[:number_of_cards]})
        else:
            return jsonify({'error': "your session has expired please login again"})

# ? PURPOSE: for retrieving list of brands and businesses


@app.route("/paypal-concept-data/v2/businesses-and-brands", methods=['POST', 'GET'])
def paypal_concept_data_v2_businesses_and_brands():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/brands_businesses_data.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'error': "your session has expired please login again"})

# ? PURPOSE: for executing transaction


@app.route("/paypal-concept-data/v2/execute-transaction", methods=['POST', 'GET'])
def paypal_concept_data_v2_execute_transaction():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        print("enteres post execute")
        token_status = json_token_validifier(request.json['hash'])
        print(token_status)
        if token_status != "invalid":
            transaction_receipt = request.json['transactionReceipt']
            transaction_status = random.choice(['successful', 'failed'])
            transaction_id = uuid4()
            transaction_date = datetime.now()
            return jsonify({'transactionReceipt': transaction_receipt, 'transactionStatus': transaction_status, 'transactionID': transaction_id, 'transactionDate': transaction_date})
        else:
            return jsonify({'error': "your session has expired please login again"})


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
