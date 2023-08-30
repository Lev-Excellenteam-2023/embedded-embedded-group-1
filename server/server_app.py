import logging

from flask import Flask, jsonify, request
import requests
from server_consts import SERVER_PORT, CLIENT_URL, DETECTOR_URL, DETECTOR_CHANGE_THRESHOLD_PATH
from db.utils_for_data import store_data

from analyzer import api_hour_with_most_birds, api_hours_with_high_birds_average

app = Flask(__name__)


@app.route('/get_alert', methods=['POST'])
def listener():
    """
    get alert from the detector
    :return:
    """
    try:
        json_data = request.json
        logging.info(f"Received alert from detector. Data: {json_data}")
        store_data(json_data)
        notify_user(json_data)
        return jsonify({"message": "alert processed successfully"})
    except Exception as e:
        logging.error(f"Failed to process alert. Error: {e}")
        return jsonify({"error": str(e)})


# function to send report to client when requested
@app.route('/get_report', methods=['GET'])
def get_report():
    """
    get request from the client to get the report
    :return: None
    """
    try:
        logging.info(f"Received request from client to get report")
        message = api_hour_with_most_birds()
        message += "\n\n"
        message += api_hours_with_high_birds_average()
        return jsonify({"message": message})
    except Exception as e:
        logging.error(f"Failed to send report. Error: {e}")
        return jsonify({"error": str(e)})


@app.route('/change_threshold', methods=['POST'])
def change_threshold():
    """
    get request from the client to change the threshold
    and send it to the detector
    :return: None
    """
    try:
        json_data = request.json
        new_threshold = json_data["threshold"]
        logging.info(f"Received request from client to change threshold to {new_threshold}")
        response = requests.post(f"{DETECTOR_URL}{DETECTOR_CHANGE_THRESHOLD_PATH}", json=json_data)
        if response.status_code == 200:
            logging.info("Threshold changed successfully.")
            return jsonify({"message": "threshold changed successfully"})
        else:
            logging.error(f"Failed to change threshold. Status code: {response.status_code}")
            return jsonify({"error": "failed to change threshold"})
    except Exception as e:
        logging.error(f"Failed to change threshold. Error: {e}")
        return jsonify({"error": str(e)})


def notify_user(json_data):
    try:
        camera = json_data.get('camera_id')
        birds_sum = json_data.get('birds_sum')
        time = json_data.get('time')
        msg = "camera {} identify {} birds at {}".format(camera, birds_sum, time)
        response = requests.post(CLIENT_URL, data=msg)
        if response.status_code == 200:
            logging.info("JSON data sent successfully.")
        else:
            logging.error(f"Failed to send JSON data. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to send JSON data. Error: {e}")


if __name__ == '__main__':
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')
    app.run(debug=True, port=SERVER_PORT)
