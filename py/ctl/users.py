import base64
import hashlib
import functools
import flask

import dao.utils
import dao.users

users_ctl = flask.Blueprint('users', __name__)


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in flask.session:
            return flask.redirect(
                flask.url_for('login_page', next=flask.request.url))
        return f(*args, **kwargs)
    return decorated_function


@users_ctl.route('/login', methods=['GET'])
def login_page():
    return flask.render_template('users/login.html')


@users_ctl.route('/login', methods=['POST'])
def login_form():
    form = flask.request.form
    if ('username' not in form) or ('password' not in form):
        return 'Something wrong'
    username, password = form['username'], form['password']
    if len(username) < 7 or len(password) < 7:
        flask.flash('Username and Password should have at least 7 symbols!')
        return flask.redirect(flask.url_for('users.login_form'))
    pwd_hash = password_hash(form['password'])
    if form['email'] == '':
        return attempt_login(username, pwd_hash)
    else:
        return attempt_register(username, pwd_hash, form['email'])


def password_hash(password):
    pwd_salted = flask.current_app.config['PWD_SALT'] + password
    pwd_digest = hashlib.sha512(pwd_salted.encode('utf-8')).digest()
    return base64.b64encode(pwd_digest)[0:32].decode('utf-8')


def attempt_login(username, password):
    uid = dao.users.find_with_creds(username, password)
    if uid is None:
        flask.flash('Wrong Username or Password!')
        return flask.redirect(flask.url_for('users.login_form'))
    return login_success()


def attempt_register(username, password, email):
    uid = dao.users.find_with_creds(username, password)
    if uid is not None:
        flask.flash('Username is already registered!')
        return flask.redirect(flask.url_for('users.login_form'))
    dao.users.insert(username, password, email)
    return login_success(username)


def login_success(username):
    flask.session['username'] = username
    flask.flash('Greetings, Mortal!')
    return flask.redirect(flask.url_for('users.dashboard'))


@users_ctl.route('/dash')
@login_required
def dashboard():
    return flask.render_template(
        'users/dashboard.html', username=flask.session['username'])


@users_ctl.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('main_page'))


@users_ctl.route('/ranking')
def ranking():
    cur = dao.utils.db_conn().cursor()
    cur.execute('select count(*) from users')
    (count,) = cur.fetchone()
    cur.close()
    return flask.render_template('users/ranking.html', user_count=count)
