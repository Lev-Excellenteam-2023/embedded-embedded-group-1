"""
this file is used to listen to the port and receive requests from the server to change bird count threshold.
"""
import logging

from flask import Flask, jsonify, request


app = Flask(__name__)
threshold = [0]


@app.route('/change_threshold', methods=['POST'])
def listener():
    """
    get alert from the detector
    :return:
    """
    try:
        global threshold
        logging.info("Received request to change threshold.")
        json_data = request.json
        new_threshold = json_data["threshold"]
        if not isinstance(new_threshold, int):
            return jsonify({"error": "threshold must be an integer"})
        elif new_threshold < 0:
            return jsonify({"error": "threshold must be positive"})
        threshold[0] = new_threshold
        logging.info(f"Threshold changed successfully to {new_threshold}.")
        return jsonify({"message": "threshold changed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


def run_listener(_threshold):
    """
    this function is used to run the listener.
    :return: None
    """
    global threshold
    threshold = _threshold
    logging.info("Starting listener.")
    app.run(debug=False, port=5009, use_reloader=False)
