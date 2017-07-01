import argparse

from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/api/v1/unknown-site')
def unknown_site_data():
    return 'Foo'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Run in debug mode')
    args = parser.parse_args()
    port = 10000
    if args.debug:
        app.run(host='127.0.0.1', port=port, debug=True, threaded=True)
    else:
        http_server = WSGIServer(('127.0.0.1', port), app)
        http_server.serve_forever()
