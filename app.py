import argparse
from flask import Flask, render_template
import requests
import time
import threading

app = Flask(__name__)


WHOAMI_SERVICE_URL = "https://httpbin.org/get"
CONTINUOUS = False
last_response = "No request has been made yet."
preparing = False

@app.route('/')
def index():
    global last_response, preparing

    if preparing:
        return render_template('index.html', data="Preparing to make a new request...")
    
    return render_template('index.html', data=last_response)

@app.route('/data')
def get_data():
    global last_response, preparing
    return "Preparing to make a new request..." if preparing else last_response


def continuous_request():
    """Background task to continuously fetch new data."""
    global last_response, preparing

    while CONTINUOUS:
        response = requests.get(WHOAMI_SERVICE_URL)
        last_response = response.text
        print(f"Sent request to {WHOAMI_SERVICE_URL}. Response: {response.text}")

        time.sleep(8)
        preparing = True
        print("Preparing to make a new request...")

        time.sleep(4)
        preparing = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--whoami_url', type=str, required=True, help='URL of the whoami service')
    parser.add_argument('--continuous', action='store_true', help='Enable continuous communication loop')
    args = parser.parse_args()
    
    WHOAMI_SERVICE_URL = args.whoami_url

    last_response = requests.get(WHOAMI_SERVICE_URL).text

    if args.continuous:
        CONTINUOUS = True
        threading.Thread(target=continuous_request, daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=80)
