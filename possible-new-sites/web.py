import json

from flask import Flask, render_template, send_from_directory, Markup, redirect, jsonify
from data import DataRetriever
from flask import request

app = Flask(__name__)

data_retriever = DataRetriever()


def parse_radius(amount):
    return round(float(amount), 2)


def get_closest_systems(x, y, z, radius=5):
    return data_retriever.get_closest_systems(x=x, y=y, z=z, radius=radius)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if '' in request.form.values():
        print('Incorrect values passed: {}'.format(request.form))
        return redirect('/')
    coordinates = [parse_radius(request.form['x']), parse_radius(request.form['y']), parse_radius(request.form['z'])]
    sites = get_closest_systems(coordinates[0], coordinates[1], coordinates[2])
    print('Results: {}'.format(sites))
    return render_template('results.html', sites=sites)


@app.route('/api/search', methods=['POST'])
def search_api():
    if '' in request.form.values():
        print('Incorrect values passed: {}'.format(request.form))
        return redirect('/')
    coordinates = [parse_radius(request.form['x']), parse_radius(request.form['y']), parse_radius(request.form['z'])]
    sites = get_closest_systems(coordinates[0], coordinates[1], coordinates[2])
    return jsonify(
        {
            'sites': sites
        }
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
