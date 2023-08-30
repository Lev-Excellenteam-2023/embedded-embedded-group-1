import logging

from flask import Flask, jsonify, request, render_template
import requests

from user.consts import SERVER_URL, SERVER_CHANGE_THR_PATH

app = Flask(__name__)

received_messages = []


@app.route('/')
def home():
    return render_template('index.html', messages=received_messages)


@app.route('/', methods=['POST'])
def root_handler():
    """
    listen to server and get the alerts from him
    :return:
    """
    try:
        msg = request.data.decode('utf-8')
        print(msg)
        received_messages.append(msg)
        return jsonify({"message": "JSON data processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get_messages', methods=['GET'])
def get_messages():
    """
    update the alerts to the screen
    :return:
    """
    return jsonify({"messages": received_messages})

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    """
    send request from the user to the server to change the threshold
    :return: None
    """
    try:
        data = request.get_json()
        new_threshold = data['threshold']
        logging.info(f"Received request from client to change threshold to {new_threshold}")
        response = requests.post(f"{SERVER_URL}{SERVER_CHANGE_THR_PATH}", json=data)
        if response.status_code == 200:
            logging.info("Threshold changed successfully.")
        return jsonify({"message": "Threshold updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    logging.basicConfig(filename='user.log', level=logging.INFO, format='%(asctime)s %(message)s')
    app.run(debug=True, port=5001)
