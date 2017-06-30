from flask import Flask, render_template, send_from_directory, Markup
from data import DataRetriever

app = Flask(__name__)

data_retriever = DataRetriever()


@app.route('/')
def index():
    sites = data_retriever.ping_edsm(system_name='HIP 15443', radii=[5.3, 2.5, 0.1])
    print(sites)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
