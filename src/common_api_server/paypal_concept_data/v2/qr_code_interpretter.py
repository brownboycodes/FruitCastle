import json
from flask import Blueprint, jsonify, render_template, request
# import os.path
import random
import qrcode
# from qrcode.image.pure import PymagingImage
# import qrcode.image.svg
from src.common_api_server.paypal_concept_data.utilities import get_json_data, json_token_validifier

qr_code_interpretter = Blueprint('qr_code_interpretter', __name__, static_url_path='/dist',
                                 static_folder='../../client/dist', template_folder='client', url_prefix='/qr-code-interpretter')


@qr_code_interpretter.route("/", methods=['GET'])
def home():
    if request.method == 'GET':

        return render_template('qr_code.html')

# ? PURPOSE: for retrieving random business in form of qr code from a list of brands and businesses


@qr_code_interpretter.route("/random", methods=['GET'])
def get_random_qr_code():
    if request.method == 'GET':

        retrieved_file_data = get_json_data(
            "src/data/paypal_concept_clone/brands_businesses_data.json")

        # data_for_qr = str(random.choice(retrieved_file_data['businesses']))
        data_for_qr = json.dumps(random.choice(retrieved_file_data['businesses']))
        print('random qr code requested data for qr')

        img = qrcode.make(data_for_qr)
        print(type(img))

        img.save(
            'src/common_api_server/client/dist/images/paypal_concept_images/qr_codes/random-qr-code.png')
        return render_template('qr_code.html', qr_code='random-qr-code.png')


@qr_code_interpretter.route("/<string:brand_name>", methods=['GET'])
def get_brand_qr_code(brand_name):
    if request.method == 'GET':

        retrieved_file_data = get_json_data(
            "src/data/paypal_concept_clone/brands_businesses_data.json")['businesses']
        filtered_data = [
            x for x in retrieved_file_data if x['name'].lower().replace(" ", "-") == brand_name]
        if len(filtered_data) != 0:
            data_for_qr = json.dumps(filtered_data[0])
            print('random qr code requested data for qr')

            img = qrcode.make(data_for_qr)
            print(type(img))

            img.save(
                f'src/common_api_server/client/dist/images/paypal_concept_images/qr_codes/{brand_name}.png')
            return render_template('qr_code.html', qr_code=f'{brand_name}.png')
        else:
            return jsonify({'error': 'brand not found'})
