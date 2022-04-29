import json
import os
import re
import jwt



# ? PURPOSE: for extracting json data from file


def get_json_data(json_file_path):
    json_file = open(json_file_path, "r")
    json_file_raw = json_file.read()
    json_file_parsed = json.loads(json_file_raw)
    return json_file_parsed


male_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/male'), (None, None, []))[2]

female_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/female'), (None, None, []))[2]


# ? FEMALE CHARACTERS
turning_red_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/female/characters/turning_red'), (None, None, []))[2]

wonder_woman_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/female/characters/wonder_woman'), (None, None, []))[2]

cat_woman_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/female/characters/cat_woman'), (None, None, []))[2]

black_widow_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/female/characters/black_widow'), (None, None, []))[2]


# ? MALE CHARACTERS
ryan_reynolds_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/male/characters/ryan'), (None, None, []))[2]

ironman_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/male/characters/ironman'), (None, None, []))[2]

batman_image_filenames = next(os.walk(
    'src/fruit_castle/client/dist/images/hadwin_images/hadwin_users/male/characters/batman'), (None, None, []))[2]


valid_email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

# secret_key_jwt = "3v9fIXKwsOn9bp4vI2amfLrSx3wJ2gF8STMtEJLjM5kPVXdWFoTPOiABiNhuGvLf0Y2hoaJm7LuCUTH5mKTayjm2338mzGgmpUUwN49IhrH9Kb4Htrb6TkPjWzeMz1RzKh8yhD2BmeuTrb2st2KQfisQs2eIs7LKQu37W68bfhVG0ryecIO0q7JK4Q1fewFHRP0RI2p0"


secret_key_jwt = os.environ.get('HADWIN_SECRET_KEY')


def decode_json_token(encoded_token):
    try:
        decoded_token = jwt.decode(
            encoded_token, secret_key_jwt, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {'apiAuthorizationError': "your session has expired please login again"}
    except jwt.InvalidTokenError:
        return {'corruptedTokenError': 'suspicious activity detected'}


def json_token_validifier(encoded_token):
    try:
        decoded_token = jwt.decode(
            encoded_token, secret_key_jwt, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "invalid"
    except jwt.InvalidTokenError:
        return "invalid"
