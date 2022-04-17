from src.fruit_castle.playpal.v3.v3_user_route import get_avatar, get_female_character_avatar, get_male_character_avatar, male_characters, female_characters
from src.fruit_castle.main import socketio
from flask_socketio import emit
from src.fruit_castle.playpal.utilities import decode_json_token, get_json_data


@socketio.on('username request', namespace='/playpal/v3')
def username_requested(username, authorization_token):
    username_status = False
    profile_pic = 'NONE'
    decoded_token = decode_json_token(authorization_token)
    if 'error' not in "".join(decoded_token.keys()).lower():
        retrieved_file_data = get_json_data(
            "src/data/playpal/local_test_user_data.json")['users']
        filtered_data = [
            x for x in retrieved_file_data if x['id'] == decoded_token['userId']]
        if len(filtered_data) != 0:
            if filtered_data[0]['username'] == username:
                if filtered_data[0]['id'] in male_characters:
                    profile_pic = get_male_character_avatar(
                        filtered_data[0]['id'])
                elif filtered_data[0]['id'] in female_characters:
                    profile_pic = get_female_character_avatar(
                        filtered_data[0]['id'])
                else:
                    profile_pic = get_avatar(
                        filtered_data[0]['gender'])
                username_status = True
            else:
                username_status = False
        emit('username status', (username_status, profile_pic),
             namespace='/playpal/v3')
    else:
        emit('error', 'something went wrong', namespace='/playpal/v3')
