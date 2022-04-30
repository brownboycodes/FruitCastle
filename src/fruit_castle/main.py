from urllib import response
from flask import Flask, jsonify, make_response, render_template
from werkzeug.exceptions import HTTPException
import json
from flask_compress import Compress
from flask_socketio import SocketIO
from flask_cors import CORS
from .hadwin.hadwin import hadwin


app = Flask(__name__, static_url_path='/dist',
            static_folder='client/dist', template_folder='client')
app.register_blueprint(hadwin)


# ? setting COMPRESSION_ALGORITHM to GZIP at COMPRESSION_LEVEL 7
app.config["COMPRESS_ALGORITHM"] = ['gzip', 'br', 'deflate']
app.config['COMPRESS_LEVEL'] = 7
app.config['COMPRESS_MIN_SIZE'] = 0.0001
# * setting COMPRESSION_ALGORITHM to default BR at default COMPRESS_BR_LEVEL 6
# * app.config["COMPRESS_ALGORITHM"] = ['br', 'gzip', 'deflate']
# * app.config['COMPRESS_BR_LEVEL'] = 8
compress = Compress()
# ? enabling CORS
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# ? enabling compression GLOBALLY
compress.init_app(app)


def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


@app.route('/')
def home():
    # return render_template("index.html")
    about_fruit_castle = {
        'project_name': 'FruitCastle',
        'version': '3.0.0',
        'description': 'backend server',
        'dependencies': ['python', 'flask', 'socket.IO', 'gzip'],
        'available_apis': ['fund_transfer_platform_prototype'],
        'github_repository': 'https://github.com/brownboycodes/FruitCastle',
        'author': 'Nabhodipta Garai',
        'social_id_username': 'brownboycodes'
    }
    return make_response(jsonify(about_fruit_castle), 200)


@app.route('/about/brownboycodes')
def about_brownboycodes():
    retrieved_file_data = get_json_data(
        "src/data/brownboycodes.json")
    return jsonify(retrieved_file_data)


# ? COMMON ERROR HANDLER FOR ALL ROUTES

@app.errorhandler(Exception)
def handle_error(e):
    error_code = 500
    error_response = ""
    if isinstance(e, HTTPException):
        error_code = e.code
    if error_code >= 100 and error_code < 200:
        error_response = '?'
    elif error_code >= 200 and error_code < 300:
        error_response = 'successful :-)'
    elif error_code >= 300 and error_code < 400:
        error_response = 'redirecting...'
    elif error_code >= 400 and error_code < 500:
        error_response = 'error on your end'
    elif error_code >= 500 and error_code < 600:
        error_response = 'error on our end'
    return make_response(
        # render_template("error_page.html", error_code=str(error_code)),
        jsonify({'error_code': error_code, 'error_message': error_response}),
        error_code
    )
