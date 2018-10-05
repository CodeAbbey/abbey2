import flask
import functools
from ctl.tasks import tasks_ctl

app = flask.Flask(__name__, static_url_path = '/s')
app.register_blueprint(tasks_ctl)

@app.errorhandler(404)
def page_not_found(e):
  return flask.render_template('404.html'), 404

@app.route('/')
def main_page():
    return flask.render_template('index.html')

@app.route('/login', methods = ['GET'])
def login_page():
    return flask.render_template('login.html')

@app.route('/login', methods = ['POST'])
def login_form():
    if not 'username' in flask.request.form:
        return 'Something wrong'
    flask.session['username'] = flask.request.form['username']
    return flask.redirect(flask.url_for('dashboard'))

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in flask.session:
            return flask.redirect(flask.url_for('login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dash')
@login_required
def dashboard():
    return flask.render_template('dashboard.html', username = flask.session['username'])

@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('main_page'))

if __name__ == '__main__':
    app.secret_key = 'super secret key for debugging'
    app.run(host='0.0.0.0', port=5000, debug=True)

