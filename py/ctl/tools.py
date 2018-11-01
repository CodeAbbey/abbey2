import hashlib
import re
import flask
import mistune

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
    dao.utils.update_blob(id, body, 'blobs')


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


@tools_ctl.route('/update_stats', methods=['GET'])
def update_stats():
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    cur.execute('replace into taskstats select * from taskstats_v', ())
    cn.commit()
    cur.execute('replace into userstats select * from userstats_v', ())
    cn.commit()
    cur.close()
    return 'ok'


@tools_ctl.route('/wiki/<pageid>')
def wiki_view(pageid):
    if re.match(r'[a-z][a-z0-9\-]*$', pageid) is None:
        flask.abort(404)
    pageid = 'wk.' + pageid + '.en'
    body = dao.utils.query_one('blobs', 'id=%s', (pageid,), 'val')
    if body is None:
        flask.abort(404)
    md = body[0].decode('utf-8')
    m = re.search(r'#\s(.+)', md)
    title = m.group(1) if m is not None else 'Wiki'
    renderer = mistune.Renderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer)
    text = markdown(md)
    return flask.render_template('wiki.html', title=title, body=text)
