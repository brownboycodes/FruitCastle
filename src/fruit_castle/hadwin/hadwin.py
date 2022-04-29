from flask import Blueprint, abort, jsonify, render_template
from src.fruit_castle.hadwin.utilities import get_json_data

from .v1.version_1 import v1
from .v2.version_2 import v2
from .v3.version_3 import v3

hadwin = Blueprint('hadwin', __name__,  url_prefix='/hadwin',static_url_path='/dist',
            static_folder='../client/dist', template_folder='client')

hadwin.register_blueprint(v1)
hadwin.register_blueprint(v2)
hadwin.register_blueprint(v3)


@hadwin.route("/")
def hadwin_home():
    # return render_template("dashboard.html", py_sent_data="hadwin concept data")
    abort(401)


@hadwin.route('/app')
def hadwin_about_app():
    retrieved_file_data = get_json_data(
        "src/data/hadwin/about_the_app.json")
    return jsonify(retrieved_file_data)
