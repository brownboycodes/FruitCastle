import re
from flask import Blueprint, jsonify, render_template, request
from datetime import datetime, timedelta, timezone
import random

import jwt

from src.common_api_server.paypal_concept_data.utilities import get_json_data, json_token_validifier, female_image_filenames, male_image_filenames, decode_json_token, secret_key_jwt, valid_email_regex

user = Blueprint('user', __name__, static_url_path='/dist',
                 static_folder='../../client/dist', template_folder='client', url_prefix='/user')


def get_avatar(gender):
    if gender == "Female":
        return random.choice(
            female_image_filenames)
    else:
        return random.choice(
            male_image_filenames)

# ? PURPOSE: to allow an already logged in user to access their account if they have a valid token


@user.route("/<int:user_id>", methods=['POST', 'GET'])
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
                    "src/data/paypal_concept_clone/local_test_user_data.json")['users']
                filtered_data = [
                    x for x in retrieved_file_data if x['id'] == user_id]
                if len(filtered_data) != 0:
                    '''if filtered_data[0]['gender'] == "Female":
                        filtered_data[0]['avatar'] = random.choice(
                            female_image_filenames)
                    else:
                        filtered_data[0]['avatar'] = random.choice(
                            male_image_filenames)'''
                    filtered_data[0]['avatar'] = get_avatar(
                        filtered_data[0]['gender'])
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


@user.route("/login", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_login():
    if request.method == 'POST':
        login_response = {'error': 'some error occurred'}
        username_or_email = request.json['userInput']
        entered_password = request.json['password']

        retrieved_file_data = get_json_data(
            "src/data/paypal_concept_clone/local_test_user_data.json")['users']
        if re.fullmatch(valid_email_regex, username_or_email):
            filtered_data = [
                x for x in retrieved_file_data if x['email'] == username_or_email]
            if len(filtered_data) != 0:
                if entered_password == filtered_data[0]['password']:
                    successful_hash = jwt.encode(
                        {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=30)}, secret_key_jwt, algorithm="HS256")
                    '''if filtered_data[0]['gender'] == "Female":
                        filtered_data[0]['avatar'] = random.choice(
                            female_image_filenames)
                    else:
                        filtered_data[0]['avatar'] = random.choice(
                            male_image_filenames)'''
                    filtered_data[0]['avatar'] = get_avatar(
                        filtered_data[0]['gender'])
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
                    '''if filtered_data[0]['gender'] == "Female":
                        filtered_data[0]['avatar'] = random.choice(
                            female_image_filenames)
                    else:
                        filtered_data[0]['avatar'] = random.choice(
                            male_image_filenames)'''
                    filtered_data[0]['avatar'] = get_avatar(
                        filtered_data[0]['gender'])
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

# ? START OF USER REGISTRATION


@user.route("/register", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_registration():
    if request.method == 'POST':
        login_response = {'error': 'some error occurred'}
        fullName = request.json['fullname']
        emailId = request.json['emailId']
        address = request.json['address']
        bank_account = request.json['bankAccount']
        entered_password = request.json['password']

        retrieved_file_data = get_json_data(
            "src/data/paypal_concept_clone/local_test_user_data.json")['users']

        filtered_data = [
            x for x in retrieved_file_data if x['email'] == emailId]
        if len(filtered_data) != 0:
            related_bank_account = [
                y for y in filtered_data[0]['bankDetails'] if y['accountNumber'] == bank_account]
            if len(related_bank_account) != 0:
                successful_hash = jwt.encode(
                    {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=30)}, secret_key_jwt, algorithm="HS256")
                del filtered_data[0]['username']
                del filtered_data[0]['avatar']
                login_response = {
                    'hash': successful_hash, 'user': filtered_data[0]}
            else:
                login_response = {'error': "details could not be verified"}
        else:
            login_response = {
                'error': "account already exists with the details provided"}

        return jsonify(login_response)

    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})

# ? END OF USER REGISTRATION


@user.route("/verify-login", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_verify_login():
    if request.method == 'POST':
        encoded_token = request.json['hash']
        decoded_token = decode_json_token(encoded_token)
        return jsonify(decoded_token)
    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})


@user.route("/verify-username", methods=['POST', 'GET'])
def paypal_concept_data_v1_user_verify_username():
    if request.method == 'POST':
        encoded_token = request.json['hash']
        requested_username = request.json['username']
        decoded_token = decode_json_token(encoded_token)
        if 'error' not in decoded_token:
            retrieved_file_data = get_json_data(
                "src/data/paypal_concept_clone/local_test_user_data.json")['users']
            filtered_data = [
                x for x in retrieved_file_data if x['id'] == decoded_token['userId']]
            if len(filtered_data) != 0:
                if filtered_data[0]['username'] == requested_username:
                    filtered_data[0]['avatar'] = get_avatar(
                        filtered_data[0]['gender'])
                    return jsonify({"success": f"your username has been set to {requested_username}", 'user': filtered_data[0]})
                else:
                    return jsonify({'error': f'the username {requested_username} is not available'})
        else:
            return jsonify({'error': 'something went wrong'})
    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})
