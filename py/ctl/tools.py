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
def blob_store(id):
    body = flask.request.get_data(cache=False)
    verify = flask.request.headers.get('X-Hash', '')
    body_hash = blob_digest(body)
    if body_hash != verify:
        return 'Method Not Allowed\r\n', 405
    update_blob(id, body)
    return 'Ok\r\n'


def update_blob(id, body):
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    query = 'insert into blobs (id, val) values (%s, %s)' \
        + ' on duplicate key update val=%s'
    cur.execute(query, (id, body, body))
    cn.commit()
    cur.close()


@tools_ctl.route('/blobs/<id>', methods=['GET'])
def blob_view(id):
    verify = flask.request.headers.get('X-Hash', '')
    id_hash = blob_digest(id.encode('utf-8'))
    if id_hash != verify:
        return 'Method not Allowed\r\n', 405
    body = dao.utils.query_one('blobs', 'id=%s', (id,), 'val')
    return ':)\r\n' if body is None else body[0].decode('utf-8')


def blob_digest(binary):
    salt = flask.current_app.config['BLOB_SALT'].encode('utf-8')
    return hashlib.sha512(salt + binary).hexdigest()
