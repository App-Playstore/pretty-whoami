import argparse
from flask import Flask, render_template
import requests

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--whoami_url', type=str, required=True, help='URL of the whoami service')
args = parser.parse_args()

WHOAMI_SERVICE_URL = args.whoami_url


@app.route('/')
def index():
    response = requests.get(WHOAMI_SERVICE_URL)
    return render_template('index.html', data=response.text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)