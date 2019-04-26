import flask

import dao.utils

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


@mgmt_ctl.route('/blobs/<id>', methods=['POST'])
def blob_store(id):
    body = flask.request.get_data(cache=False)
    update_blob(id, body)
    return 'Ok\r\n'


def update_blob(id, body):
    dao.utils.update_blob(id, body, 'blobs')


@mgmt_ctl.route('/blobs/<id>', methods=['GET'])
def blob_view(id):
    body = dao.utils.query_one('blobs', 'id=%s', (id,), 'val')
    if body is None:
        return ('', 204)
    else:
        return body[0].decode('utf-8')
