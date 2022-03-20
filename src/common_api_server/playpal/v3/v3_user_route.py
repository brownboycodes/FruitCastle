from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta, timezone
from src.common_api_server.playpal.utilities import *

user_v3 = Blueprint('user', __name__, static_url_path='/dist',
                 static_folder='../../client/dist', template_folder='client', url_prefix='/user')


female_characters = [7426, 5998, 3938, 7029]
male_characters = [7587, 3421, 6898]


def get_avatar(gender):
    if gender == "Female":
        return random.choice(
            female_image_filenames)
    else:
        return random.choice(
            male_image_filenames)


def get_male_character_avatar(id):
    avatar_path = "characters"
    if id == 7587:
        avatar_path += '/batman/'+random.choice(batman_image_filenames)
    elif id == 3421:
        avatar_path += '/ironman/'+random.choice(ironman_image_filenames)
    elif id == 6898:
        avatar_path += '/ryan/'+random.choice(ryan_reynolds_image_filenames)
    return avatar_path


def get_female_character_avatar(id):
    avatar_path = "characters"
    if id == 7426:
        avatar_path += '/turning_red/' + \
            random.choice(turning_red_image_filenames)
    elif id == 5998:
        avatar_path += '/wonder_woman/' + \
            random.choice(wonder_woman_image_filenames)
    elif id == 3938:
        avatar_path += '/cat_woman/'+random.choice(cat_woman_image_filenames)
    elif id == 7029:
        avatar_path += '/black_widow/' + \
            random.choice(black_widow_image_filenames)
    return avatar_path




# ? PURPOSE: to allow an already logged in user to access their account if they have a valid token


@user_v3.route("/<int:user_id>", methods=['POST', 'GET'])
def playpal_v3_get_user_by_id(user_id):
    login_response = {"error": "something went wrong"}
    if request.method == 'GET':
        login_response = {"error": "this is a GET request"}
    if request.method == 'POST':
        received_hash = request.json['hash']
        token_status = json_token_validifier(received_hash)
        if token_status != "invalid":
            if token_status['userId'] == user_id:
                retrieved_file_data = get_json_data(
                    "src/data/playpal/local_test_user_data.json")['users']
                filtered_data = [
                    x for x in retrieved_file_data if x['id'] == user_id]
                if len(filtered_data) != 0:
                    if filtered_data[0]['id'] in male_characters:
                        filtered_data[0]['avatar'] = get_male_character_avatar(
                            filtered_data[0]['id'])
                    elif filtered_data[0]['id'] in female_characters:
                        filtered_data[0]['avatar'] = get_female_character_avatar(
                            filtered_data[0]['id'])
                    else:
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


@user_v3.route("/login", methods=['POST', 'GET'])
def playpal_v3_user_login():
    if request.method == 'POST':
        login_response = {'error': 'some error occurred'}
        username_or_email = request.json['userInput']
        entered_password = request.json['password']

        retrieved_file_data = get_json_data(
            "src/data/playpal/local_test_user_data.json")['users']
        if re.fullmatch(valid_email_regex, username_or_email):
            filtered_data = [
                x for x in retrieved_file_data if x['email'] == username_or_email]
            if len(filtered_data) != 0:
                if entered_password == filtered_data[0]['password']:
                    successful_hash = jwt.encode(
                        {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(hours=1)}, secret_key_jwt, algorithm="HS256")
                    if filtered_data[0]['id'] in male_characters:
                        filtered_data[0]['avatar'] = get_male_character_avatar(
                            filtered_data[0]['id'])
                    elif filtered_data[0]['id'] in female_characters:
                        filtered_data[0]['avatar'] = get_female_character_avatar(
                            filtered_data[0]['id'])
                    else:
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
                        {'userId': filtered_data[0]['id'], 'exp': datetime.now(tz=timezone.utc)+timedelta(hours=1)}, secret_key_jwt, algorithm="HS256")
                    if filtered_data[0]['id'] in male_characters:
                        filtered_data[0]['avatar'] = get_male_character_avatar(
                            filtered_data[0]['id'])
                    elif filtered_data[0]['id'] in female_characters:
                        filtered_data[0]['avatar'] = get_female_character_avatar(
                            filtered_data[0]['id'])
                    else:
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


@user_v3.route("/verify-username", methods=['POST', 'GET'])
def playpal_v3_user_verify_username():
    if request.method == 'POST':
        encoded_token = request.json['hash']
        requested_username = request.json['username']
        decoded_token = decode_json_token(encoded_token)
        if 'error' not in decoded_token:
            retrieved_file_data = get_json_data(
                "src/data/playpal/local_test_user_data.json")['users']
            filtered_data = [
                x for x in retrieved_file_data if x['id'] == decoded_token['userId']]
            if len(filtered_data) != 0:
                if filtered_data[0]['username'] == requested_username:
                    if filtered_data[0]['id'] in male_characters:
                        filtered_data[0]['avatar'] = get_male_character_avatar(
                            filtered_data[0]['id'])
                    elif filtered_data[0]['id'] in female_characters:
                        filtered_data[0]['avatar'] = get_female_character_avatar(
                            filtered_data[0]['id'])
                    else:
                        filtered_data[0]['avatar'] = get_avatar(
                            filtered_data[0]['gender'])
                    return jsonify({"success": f"your username has been set to {requested_username}", 'user': filtered_data[0]})
                else:
                    return jsonify({'error': f'the username {requested_username} is not available'})
        else:
            return jsonify({'error': 'something went wrong'})
    if request.method == 'GET':
        return jsonify({'error': 'this is a GET request'})