import flask

mgmt_ctl = flask.Blueprint('mgmt', __name__)


@mgmt_ctl.before_request
def check_access():
    session = flask.session
    if 'username' not in session or 'mgm' not in session['userflags']:
        flask.abort(404)


@mgmt_ctl.route('/')
def mgmt_main():
    return 'Hi, this is a mgmt page!'


@mgmt_ctl.route('/blobs')
def mgmt_blobs():
    return flask.render_template('mgmt/blobs.html')
