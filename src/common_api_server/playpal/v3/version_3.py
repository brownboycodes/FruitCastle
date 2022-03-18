from flask import Blueprint, jsonify, render_template, request
from .v3_user_route import user_v3
from src.common_api_server.playpal.utilities import get_json_data, json_token_validifier

v3 = Blueprint('v3', __name__, static_url_path='/dist',
               static_folder='../../client/dist', template_folder='client', url_prefix='/v3')
v3.register_blueprint(user_v3)


@v3.route("/")
def test_socket():
    return jsonify({'message': 'sockets active'})


# ? PURPOSE: for extracting contacts of the user


@v3.route("/all-contacts", methods=['POST', 'GET'])
def playpal_v3_all_contacts():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":

            users_wallet_address = [
                x for x in get_json_data(
                    "src/data/playpal/local_test_user_data.json")['users'] if x['id'] == token_status['userId']][0]['walletAddress']

            retrieved_file_data = get_json_data(
                "src/data/playpal/local_contacts.json")

            filtered_contact_data = [
                x for x in retrieved_file_data['contacts'] if x['walletAddress'] != users_wallet_address]

            return jsonify({"contacts": filtered_contact_data})
        else:
            return jsonify({'error': "your session has expired please login again"})

"""
@v3.route("/active-socket")
def test_active_socket():
    return render_template('test_socket.html')
"""


