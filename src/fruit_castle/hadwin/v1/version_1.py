import random

from flask import Blueprint, jsonify, make_response, send_from_directory, request
from src.fruit_castle.hadwin.utilities import get_json_data, json_token_validifier

from .user_route import user

v1 = Blueprint('v1', __name__, static_url_path='/dist',
               static_folder='../../client/dist', template_folder='client', url_prefix='/v1')
v1.register_blueprint(user)


@v1.route("/")
def hadwin_v1():
    response_for_route = {
        "error": "please mention exactly what you want from version 1 of the hadwin API"}
    return jsonify(response_for_route)


@v1.route("/all-data", methods=['POST', 'GET'])
def hadwin_v1_all_data():
    if request.method == 'POST':
        return make_response(jsonify({"error": "this is a POST request"}), 403)
    if request.method == 'GET':
        token_status = json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data("src/data/users.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


@v1.route("/all-users", methods=['POST', 'GET'])
def hadwin_v1_all_users():
    if request.method == 'POST':
        return make_response(jsonify({"error": "this is a GET request"}), 403)
    if request.method == 'GET':
        token_status = json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/hadwin/local_test_user_data.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


# ? PURPOSE: for extracting transaction records


@v1.route("/all-transactions", methods=['POST', 'GET'])
def hadwin_v1_all_transactions():
    if request.method == 'POST':
        return make_response(jsonify({"error": "this is a POST request"}), 403)
    if request.method == 'GET':
        token_status = json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/hadwin/transactions.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})

# ? PURPOSE: for extracting contacts of the user


@v1.route("/all-contacts", methods=['POST', 'GET'])
def hadwin_v1_all_contacts():
    if request.method == 'POST':
        return make_response(jsonify({"error": "this is a POST request"}), 403)
    if request.method == 'GET':
        token_status = json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/hadwin/local_contacts.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})

# ? PURPOSE: for retrieving cards available for the user


@v1.route("/available-cards", methods=['POST', 'GET'])
def hadwin_v1_available_cards():
    if request.method == 'POST':
        return make_response(jsonify({"error": "this is a POST request"}), 403)
    if request.method == 'GET':
        token_status = json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/hadwin/card_data.json")
            available_cards = retrieved_file_data['availableCards']
            random.shuffle(available_cards)
            number_of_cards = random.choice(range(1, 3))
            return jsonify({'availableCards': available_cards[:number_of_cards]})
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


'''@v1.route('/docs')
def hadwin_v1_docs():
    return send_from_directory("../docs/hadwin/v1", "hadwin_v1_wiki.md")'''
