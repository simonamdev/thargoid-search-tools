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
    radii = [parse_radius(request.form['radius1']), parse_radius(request.form['radius2']), parse_radius(request.form['radius3'])]
    sites = data_retriever.ping_edsm(system_name=request.form['system'], radii=radii)
    print('Results: {}'.format(sites))
    return render_template('results.html', sites=sites)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
