from flask import Flask, render_template, send_from_directory, Markup, redirect
from data import DataRetriever
from flask import request

app = Flask(__name__)

data_retriever = DataRetriever()


def parse_radius(amount):
    return round(float(amount), 2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if '' in request.form.values():
        print('Incorrect values passed: {}'.format(request.form))
        return redirect('/')
    coordinates = [parse_radius(request.form['x']), parse_radius(request.form['y']), parse_radius(request.form['z'])]
    sites = data_retriever.get_closest_systems(x=coordinates[0], y=coordinates[1], z=coordinates[2], radius=5)
    print('Results: {}'.format(sites))
    return render_template('results.html', sites=sites)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
