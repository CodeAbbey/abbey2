import flask
from ctl.tasks import tasks_ctl

app = flask.Flask(__name__, static_url_path = '/s')
app.register_blueprint(tasks_ctl)

@app.route('/')
def main_page():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

