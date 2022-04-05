from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
import random
from uuid import uuid4
from src.common_api_server.playpal.utilities import get_json_data, json_token_validifier
from .qr_code_interpretter import qr_code_interpretter

v2 = Blueprint('v2', __name__, static_url_path='/dist',
               static_folder='../../client/dist', template_folder='client', url_prefix='/v2')
v2.register_blueprint(qr_code_interpretter)

@v2.route("/")
def playpal_v2():
    response_for_route = {
        "error": "please mention exactly what you want from version 2 of the playpal API"}
    return jsonify(response_for_route)

# ? PURPOSE: for retrieving list of brands and businesses


@v2.route("/businesses-and-brands", methods=['POST', 'GET'])
def playpal_v2_businesses_and_brands():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':
        token_status = json_token_validifier(request.json['hash'])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/playpal/brands_businesses_data.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


# ? PURPOSE: for executing transaction


@v2.route("/execute-transaction", methods=['POST', 'GET'])
def playpal_v2_execute_transaction():
    if request.method == 'GET':
        return jsonify({"error": "this is a GET request"})
    if request.method == 'POST':

        token_status = json_token_validifier(request.json['hash'])
        print(token_status)
        if token_status != "invalid":
            transaction_receipt = request.json['transactionReceipt']
            # ? MANIPULATING RANDOMNESS TO OBTAIN 66.666 % POSITIVE OUTCOME
            transaction_status = random.choice(['successful','successful', 'failed'])
            transaction_id = uuid4()
            
            transaction_date = f'{datetime.now()}'
            transaction_receipt['transactionID'] = transaction_id
            transaction_receipt['transactionDate'] = transaction_date
            return jsonify({'transactionReceipt': transaction_receipt, 'transactionStatus': transaction_status})
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


