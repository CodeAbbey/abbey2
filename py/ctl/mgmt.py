import flask

import dao.tasks
import dao.utils

mgmt_ctl = flask.Blueprint('mgmt', __name__)


@mgmt_ctl.before_request
def check_access():
    session = flask.session
    if 'username' not in session or 'mgm' not in session['userflags']:
        flask.abort(404)


@mgmt_ctl.route('/')
def mgmt_main():
    return flask.render_template('mgmt/index.html')


@mgmt_ctl.route('/task_update', methods=['POST'])
def task_update():
    tid = flask.request.form['taskid']
    title = flask.request.form['tasktitle']
    msg = "task #%s was " % tid
    if title != 'DELETE-IT-PLEASE':
        dao.tasks.update_title(tid, title)
        msg += "named '%s'" % title
    else:
        dao.tasks.delete_title(tid)
        msg += "deleted :("
    return flask.render_template(
        'mgmt/result.html', msg=msg)


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


def blob_list_view(id):
    body = dao.utils.query_many(
            'blobs', 'id', None, '*', 'LIKE \'' + id + '\'')
    list_str = ''
    if body is None:
        return ('', 204)
    for blob in body:
        list_str += blob[0] + '\n'
    return list_str


@mgmt_ctl.route('/blobs/<id>', methods=['GET'])
def blob_view(id):
    if '*' in id:
        id = id.replace('*', '%')
        return blob_list_view(id)
    body = dao.utils.query_one('blobs', 'id=%s', (id,), 'val')
    if body is None:
        return ('', 204)
    else:
        return body[0].decode('utf-8')
