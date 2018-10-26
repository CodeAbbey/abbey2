import hashlib
import flask

import dao.users
import dao.utils

tools_ctl = flask.Blueprint('tools', __name__)


@tools_ctl.route('/mess')
def action_log():
    data = dao.users.action_log_recent(100)
    return flask.render_template('mess.html', data=data)


@tools_ctl.route('/blobs/<id>', methods=['POST'])
def blobs(id):
    body = flask.request.get_data(cache=False)
    verify = flask.request.headers.get('X-Hash', '')
    salt = flask.current_app.config['BLOB_SALT'].encode('utf-8')
    body_hash = hashlib.sha512(salt + body).hexdigest()
    if body_hash != verify:
        return 'Not Found', 404
    update_blob(id, body)
    return 'Ok'


def update_blob(id, body):
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    query = 'insert into blobs (id, val) values (%s, %s)' \
        + ' on duplicate key update val=%s'
    cur.execute(query, (id, body, body))
    cn.commit()
    cur.close()
