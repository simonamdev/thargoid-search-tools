import argparse

from flask import Flask, render_template, redirect, jsonify
from data import DataRetriever
from flask import request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

data_retriever = DataRetriever()


def parse_distance(amount):
    return round(float(amount), 2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if '' in request.form.values():
        print('Incorrect values passed: {}'.format(request.form))
        return redirect('/')
    coordinates = [parse_distance(request.form['x']), parse_distance(request.form['y']), parse_distance(request.form['z'])]
    distances = [parse_distance(request.form['a']), parse_distance(request.form['b']), parse_distance(request.form['c'])]
    sites = data_retriever.get_possible_systems(coordinates=coordinates, distances=distances)
    print('Results: {}'.format(sites))
    return render_template('results.html', sites=sites)

#
# @app.route('/api/search', methods=['POST'])
# def search_api():
#     if '' in request.form.values():
#         print('Incorrect values passed: {}'.format(request.form))
#         return redirect('/')
#     coordinates = [parse_distance(request.form['x']), parse_distance(request.form['y']), parse_distance(request.form['z'])]
#     sites = get_closest_systems(coordinates[0], coordinates[1], coordinates[2])
#     return jsonify(
#         {
#             'sites': sites
#         }
#     )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Run in debug mode')
    args = parser.parse_args()
    if args.debug:
        app.run(host='127.0.0.1', port=3000, debug=True, threaded=True)
    else:
        http_server = WSGIServer(('127.0.0.1', 3000), app)
        http_server.serve_forever()
