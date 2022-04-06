from flask import Blueprint, abort, jsonify, render_template
from src.fruit_castle.playpal.utilities import get_json_data

from .v1.version_1 import v1
from .v2.version_2 import v2
from .v3.version_3 import v3

playpal = Blueprint('playpal', __name__,  url_prefix='/playpal',static_url_path='/dist',
            static_folder='../client/dist', template_folder='client')

playpal.register_blueprint(v1)
playpal.register_blueprint(v2)
playpal.register_blueprint(v3)


@playpal.route("/")
def playpal_home():
    # return render_template("dashboard.html", py_sent_data="PlayPal concept data")
    abort(401)


@playpal.route('/app')
def playpal_about_app():
    retrieved_file_data = get_json_data(
        "src/data/playpal/about_the_app.json")
    return jsonify(retrieved_file_data)
