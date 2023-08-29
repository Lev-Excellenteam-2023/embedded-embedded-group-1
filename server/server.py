from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

BIRDS_THRESHOLD = 5


@app.route('/')
def home():
    return "hello"


#  json file{camera_id, time, birds_sum}
@app.route('/get_alert', methods=['POST'])
def listener():
    """
    get alert from the detector
    :return:
    """
    try:
        json_data = request.json
        print(json_data)
        notify_user(json_data)
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
    app.run(debug=True)
