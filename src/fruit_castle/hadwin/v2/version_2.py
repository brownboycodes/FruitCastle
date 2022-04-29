from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone
import random
from uuid import uuid4
from src.fruit_castle.hadwin.utilities import get_json_data, json_token_validifier
from .qr_code_interpretter import qr_code_interpretter

v2 = Blueprint('v2', __name__, static_url_path='/dist',
               static_folder='../../client/dist', template_folder='client', url_prefix='/v2')
v2.register_blueprint(qr_code_interpretter)

@v2.route("/")
def hadwin_v2():
    response_for_route = {
        "error": "please mention exactly what you want from version 2 of the hadwin API"}
    return jsonify(response_for_route)

# ? PURPOSE: for retrieving list of brands and businesses


@v2.route("/businesses-and-brands", methods=['POST', 'GET'])
def hadwin_v2_businesses_and_brands():
    if request.method == 'GET':
        token_status=json_token_validifier(request.headers["Authorization"])
        if token_status != "invalid":
            retrieved_file_data = get_json_data(
                "src/data/hadwin/brands_businesses_data.json")
            return jsonify(retrieved_file_data)
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})
    else:
        return make_response(jsonify({"error": "this is a POST request"}),403)


# ? PURPOSE: for executing transaction


@v2.route("/execute-transaction", methods=['POST', 'GET'])
def hadwin_v2_execute_transaction():
    if request.method == 'GET':
        return make_response(jsonify({"error": "this is a GET request"}),403)
    if request.method == 'POST':
        token_status = json_token_validifier(request.headers["Authorization"])
        # print(token_status)
        if token_status != "invalid":
            transaction_receipt = request.json['transactionReceipt']
            # ? MANIPULATING RANDOMNESS TO OBTAIN 66.666 % PROBABILITY FOR A POSITIVE OUTCOME
            transaction_status = random.choice(['successful','successful', 'failed'])
            transaction_id = uuid4()
            
            transaction_date = f'{datetime.now()}'
            transaction_receipt['transactionID'] = transaction_id
            transaction_receipt['transactionDate'] = transaction_date
            return jsonify({'transactionReceipt': transaction_receipt, 'transactionStatus': transaction_status})
        else:
            return jsonify({'apiAuthorizationError': "your session has expired please login again"})


