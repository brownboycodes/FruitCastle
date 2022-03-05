from src.common_api_server.paypal_concept_data.v1.user_route import get_avatar
from src.common_api_server.main import socketio
from flask_socketio import emit
from src.common_api_server.paypal_concept_data.utilities import decode_json_token, get_json_data


@socketio.on('username request', namespace='/paypal-concept-data/v3')
def username_requested(username, hash):
    username_status = False
    profile_pic = 'NONE'
    decoded_token = decode_json_token(hash)
    if 'error' not in decoded_token:
        retrieved_file_data = get_json_data(
            "src/data/paypal_concept_clone/local_test_user_data.json")['users']
        filtered_data = [
            x for x in retrieved_file_data if x['id'] == decoded_token['userId']]
        if len(filtered_data) != 0:
            if filtered_data[0]['username'] == username:
                profile_pic = get_avatar(
                    filtered_data[0]['gender'])
                username_status = True
            else:
                username_status = False
        emit('username status', (username_status, profile_pic),
            namespace='/paypal-concept-data/v3')
    else:
        emit('error', 'something went really wrong',namespace='/paypal-concept-data/v3')
    
