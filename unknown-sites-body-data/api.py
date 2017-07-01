import argparse

from flask import Flask, jsonify, request
from flask import json
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
data = {}
data_file_path = 'us_data.json'


def load_data():
    with open(data_file_path, 'r') as data_file:
        global data
        data = json.loads(data_file.read())


@app.route('/api/v1/unknown-site')
def unknown_site_data():
    return jsonify(
        {
            'data': data
        }
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Run in debug mode')
    args = parser.parse_args()
    load_data()
    port = 10000
    if args.debug:
        app.run(host='127.0.0.1', port=port, debug=True, threaded=True)
    else:
        http_server = WSGIServer(('127.0.0.1', port), app)
        http_server.serve_forever()
