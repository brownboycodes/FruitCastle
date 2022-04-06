from flask import Flask, jsonify, make_response, render_template
from werkzeug.exceptions import HTTPException
import json
from flask_compress import Compress
from flask_socketio import SocketIO
from flask_cors import CORS
from .playpal.playpal import playpal


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')
app.register_blueprint(playpal)


#? setting COMPRESSION_ALGORITHM to GZIP at default COMPRESSION_LEVEL 6
app.config["COMPRESS_ALGORITHM"] = ['gzip', 'br', 'deflate']
compress = Compress()
#? enabling CORS
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
#? enabling compression GLOBALLY
compress.init_app(app)

def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about/brownboycodes')
def about_brownboycodes():
    retrieved_file_data = get_json_data(
        "src/data/brownboycodes.json")
    return jsonify(retrieved_file_data)


# ? COMMON ERROR HANDLER FOR ALL ROUTES

@app.errorhandler(Exception)
def handle_error(e):
    error_code = 500
    if isinstance(e, HTTPException):
        error_code = e.code
    return make_response(
        render_template("error_page.html", error_code=str(error_code)),
        error_code
    )
