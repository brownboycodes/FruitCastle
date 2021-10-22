import json

json_file=open("src/data/users.json","r")
json_file_raw=json_file.read()
json_file_parsed=json.loads(json_file_raw)

@app.route("/paypal-concept-data/v1/all-data")
def paypal_concept_data_v1_all_data():
    return jsonify(json_file_parsed)