import flask
app = flask.Flask(__name__, static_url_path = '/s')

@app.route('/')
def hello_world():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

