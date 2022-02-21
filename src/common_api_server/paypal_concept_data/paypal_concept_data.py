from flask import Blueprint, abort, jsonify, render_template
from src.common_api_server.paypal_concept_data.utilities import get_json_data

from .v1.version_1 import v1
from .v2.version_2 import v2

paypal_concept_data = Blueprint('paypal-concept-data', __name__,  url_prefix='/paypal-concept-data',static_url_path='/dist',
            static_folder='../client/dist', template_folder='client')

paypal_concept_data.register_blueprint(v1)
paypal_concept_data.register_blueprint(v2)



@paypal_concept_data.route("/")
def paypal_concept_data_home():
    # return render_template("dashboard.html", py_sent_data="PayPal concept data")
    abort(401)


@paypal_concept_data.route('/app')
def paypal_concept_data_about_app():
    retrieved_file_data = get_json_data(
        "src/data/paypal_concept_clone/about_the_app.json")
    return jsonify(retrieved_file_data)
