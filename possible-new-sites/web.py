from flask import Flask, render_template, send_from_directory, Markup, redirect
from data import DataRetriever
from flask import request

app = Flask(__name__)

data_retriever = DataRetriever()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if '' in request.form.values():
        print('Incorrect values passed: {}'.format(request.form))
        return redirect('/')
    radii = [int(request.form['radius1']), int(request.form['radius2']), int(request.form['radius3'])]
    sites = data_retriever.ping_edsm(system_name=request.form['system'], radii=radii)
    print('Results: {}'.format(sites))
    return render_template('results.html', sites=sites)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
