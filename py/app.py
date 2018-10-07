import os
import json
import flask
from ctl.tasks import tasks_ctl
from ctl.users import users_ctl
import dao.utils


app = flask.Flask(__name__, static_url_path='/s')
app.register_blueprint(tasks_ctl)
app.register_blueprint(users_ctl)


@app.route('/')
def main_page():
    return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


@app.teardown_appcontext
def teardown(error):
    dao.utils.db_close()


def config():
    path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(path + '/config.json') as cfg_json:
        cfg = json.load(cfg_json)
        for key in cfg:
            app.config[key] = os.environ.get(key, default=cfg[key])


config()
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'dummy-key'
    app.run(host='0.0.0.0', port=5000, debug=True)
