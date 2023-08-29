import logging

from flask import Flask, jsonify, request
import requests
from server.server_consts import SERVER_PORT
from db.utils_for_data import store_data

app = Flask(__name__)




@app.route('/get_alert', methods=['POST'])
def listener():
    """
    get alert from the detector
    :return:
    """
    try:
        logging.info("Received alert from detector.")
        json_data = request.json
        store_data(json_data)
        # notify_user(json_data)
        #database.savedata(json_data)
        return jsonify({"message": "alert processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


def notify_user(json_data):
    try:
        # Replace this URL with the URL of the Control Tower
        client_url = "http://127.0.0.1:5000"

        msg="camera {} identify {} birds".format(json_data.get('camera_id'),json_data.get('birds_sum'))
        response = requests.post(client_url, msg)
        if response.status_code == 200:
            print("JSON data sent successfully to the client.")
        else:
            print(f"Failed to send JSON data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending JSON data: {str(e)}")


if __name__ == '__main__':
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')
    app.run(debug=True, port=SERVER_PORT)
