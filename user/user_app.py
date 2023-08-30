from flask import Flask, jsonify, request, render_template
import requests


app = Flask(__name__)

received_messages = []


@app.route('/')
def home():
    return render_template('index.html', messages=received_messages)


@app.route('/', methods=['POST'])
def root_handler():
    try:
        msg = request.data.decode('utf-8')
        print(msg)
        received_messages.append(msg)  # Store the received message
        # Handle the JSON data and respond accordingly
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


if __name__ == '__main__':
    app.run(debug=True, port=5001)
