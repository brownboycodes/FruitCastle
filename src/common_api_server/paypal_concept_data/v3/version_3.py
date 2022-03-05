
from flask import Blueprint, jsonify


v3 = Blueprint('v3', __name__, static_url_path='/dist',
               static_folder='../../client/dist', template_folder='client', url_prefix='/v3')

@v3.route("/")
def test_socket():
    return jsonify({'message':'sockets active'})



'''@v3.route("/active-socket")
def test_active_socket():
    return render_template('test_socket.html')'''