import logging

from flask import Flask, jsonify, request
import requests
from server_consts import SERVER_PORT, CLIENT_URL, DETECTORS_URLS, DETECTOR_CHANGE_THRESHOLD_PATH
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


@app.route('/get_report', methods=['POST'])
def get_report():
    """
    get request from the client to get the hour with the most birds in the recent days
    :return: None
    """
    try:
        json_data = request.json
        num_of_days = json_data['numOfDays']
        logging.info(f"Received request from client to get report")
        message = api_hour_with_most_birds(num_of_days)
        message += "\n\n"
        return jsonify({"message": message})
    except Exception as e:
        logging.error(f"Failed to send report. Error: {e}")
        return jsonify({"error": str(e)})

@app.route('/get_report_avg', methods=['POST'])
def get_report_avg():
    """
    get request from the client to get the report of the hours
    with average of observed birds higher than some number
    :return: None
    """
    try:
        json_data = request.json
        num_of_birds = json_data['numOfBirds']
        logging.info(f"Received request from client to get report")
        message = api_hours_with_high_birds_average(num_of_birds=num_of_birds)
        message += "\n\n"
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
        for detector_url in DETECTORS_URLS:
            try:
                requests.post(f"{detector_url}{DETECTOR_CHANGE_THRESHOLD_PATH}", json=json_data)
                logging.info(f"Threshold changed successfully to {new_threshold}. In detector: {detector_url}")
            except Exception as e:
                logging.error(f"Failed to change threshold. Error: {e}. In detector: {detector_url}")
        return jsonify({"message": "Threshold updated successfully"})
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
