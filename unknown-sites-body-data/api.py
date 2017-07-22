import argparse

from flask import Flask, jsonify, request
from flask import json, abort
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
site_data = {}
data_file_path = 'us_data.json'


def load_data():
    with open(data_file_path, 'r') as data_file:
        global site_data
        site_data = json.loads(data_file.read())
    print('Loaded data for {} sites'.format(len(site_data)))


def get_site_data(system_name, body_name):
    global site_data
    if system_name is None and body_name is None:
        return site_data
    # If there isn't the key present, then there is no data present
    if system_name.upper() not in site_data.keys():
        return None
    data = adapt_site_data(system_data=site_data[system_name], system_name=system_name)
    return data


def adapt_site_data(system_data, system_name):
    data = system_data['planets'][0]['data']
    data['body'] = system_data['planets'][0]['body'].upper()
    data['system'] = system_name.upper()
    data['full_name'] = system_data['planets'][0]['full_name'].upper()
    return data


def get_available_sites():
    available_sites = {}
    for site in site_data:
        if site['system'] not in available_sites.keys():
            available_sites[site['system']] = []
        available_sites[site['system']].append(site['body'])
    return available_sites


@app.route('/v1/unknown-sites')
def unknown_site_data():
    system_name = request.args.get('system')
    body_name = request.args.get('body')
    print('Params: {} {}'.format(system_name, body_name))
    return_site_data = get_site_data(system_name=system_name.upper(), body_name=body_name.upper())
    if return_site_data is None:
        return abort(503)
    return jsonify(
        {
            'data': return_site_data
        }
    )


@app.route('/v1/unknown-sites/available')
def available_sites_data():
    return jsonify(
        get_available_sites()
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
