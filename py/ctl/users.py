import base64
import hashlib
import flask
import re

import dao.tasks
import dao.utils
import dao.users
import utils.web

users_ctl = flask.Blueprint('users', __name__)


@users_ctl.route('/login', methods=['GET'])
def login_page():
    return flask.render_template('users/login.html')


@users_ctl.route('/login', methods=['POST'])
def login_form():
    form = flask.request.form
    if ('username' not in form) or ('password' not in form):
        return 'Something wrong'
    username, password = form['username'].lower(), form['password']
    err = check_creds_format_error(username, password)
    if err is not None:
        flask.flash(err)
        return flask.redirect(flask.url_for('users.login_form'))
    pwd_hash = password_hash(password)
    if form['email'] == '':
        return attempt_login(username, pwd_hash)
    else:
        return attempt_register(username, pwd_hash, form['email'])


def check_creds_format_error(username, password):
    if len(username) < 4 or len(username) > 31:
        return 'Please make username between 4..31 chars'
    t = re.sub(r'[a-z0-9\-\.\_]', '', username)
    if t != '':
        return 'Username: letters, digits, dash, dot and underscore'
    if len(password) < 7:
        return 'Please create password at least 7 chars'
    t = re.sub(r'[A-Za-z0-9\-\.\!\@\#\$\%\^\&\*\(\)\_]+', '', password)
    if t != '':
        return 'Password allows letters, digits and some punctuation'
    return None


def password_hash(password):
    pwd_salted = flask.current_app.config['PWD_SALT'] + password
    pwd_digest = hashlib.sha512(pwd_salted.encode('utf-8')).digest()
    return base64.b64encode(pwd_digest)[0:32].decode('utf-8')


def attempt_login(username, password):
    uid = dao.users.find_with_creds(username, password)
    if uid is None:
        flask.flash('Wrong Username or Password!')
        return flask.redirect(flask.url_for('users.login_form'))
    return login_success(username, uid)


def attempt_register(username, password, email):
    uid = dao.users.find_with_creds(username)
    if uid is not None:
        flask.flash('Username is already registered!')
        return flask.redirect(flask.url_for('users.login_form'))
    dao.users.insert(username, password, email)
    uid = dao.users.find_with_creds(username)
    return login_success(username, uid, True)


def login_success(username, uid, newcomer=False):
    flask.session['username'] = username
    flask.session['userid'] = uid
    flags = dao.users.get_flags(uid)
    flask.session['userflags'] = flags
    flask.flash('Greetings, Mortal!')
    if 'inv' not in flags:
        dao.users.action_log_write(uid, 'LOG', '' if not newcomer else 'new')
    return flask.redirect(flask.url_for('users.dashboard'))


@users_ctl.route('/dash')
@utils.web.login_required
def dashboard():
    tasks = dao.tasks.what_user_tried(flask.session['userid'])
    return flask.render_template(
        'users/dashboard.html',
        username=flask.session['username'],
        tasks=tasks)


@users_ctl.route('/profile/<username>')
def profile(username):
    uid = dao.users.find_with_creds(username)
    if uid is None:
        flask.abort(404)
    print('user found: ' + str(uid))
    tasks = dao.tasks.what_user_tried(uid)
    cats = dao.utils.query_many(
        'userstats', 'userid=%s', (uid,), 'cat,cnt,cost')
    return flask.render_template(
        'users/profile.html', username=username, tasks=tasks, cats=cats)


@users_ctl.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('main_page'))


@users_ctl.route('/ranking')
def ranking():
    tops = dao.utils.query_many(
        "users u join usertop s on u.id=s.userid "
        + "join tasks t on concat('!', s.cat) = t.id",
        None, (),
        'username,cat,cnt,cost, title', 'order by cat, cost desc')
    data = {}
    for rec in tops:
        cat = rec[1]
        if cat not in data:
            data[cat] = []
        data[cat].append(rec)
    return flask.render_template('users/ranking.html', users=data)
