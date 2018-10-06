import os
import json
import flask
import functools
from ctl.tasks import tasks_ctl
import dao.utils


app = flask.Flask(__name__, static_url_path='/s')
app.register_blueprint(tasks_ctl)


@app.route('/')
def main_page():
    return flask.render_template('index.html')


@app.route('/login', methods=['GET'])
def login_page():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def login_form():
    if 'username' not in flask.request.form:
        return 'Something wrong'
    flask.session['username'] = flask.request.form['username']
    return flask.redirect(flask.url_for('dashboard'))


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in flask.session:
            return flask.redirect(
                flask.url_for('login_page', next=flask.request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/dash')
@login_required
def dashboard():
    return flask.render_template(
        'dashboard.html', username=flask.session['username'])


@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('main_page'))


@app.route('/dbtest')
def dbtest():
    cur = dao.utils.db_conn().cursor()
    cur.execute('select count(*) from users')
    (count,) = cur.fetchone()
    cur.close()
    return 'Total users: ' + str(count)


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
