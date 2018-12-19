import hashlib
import json
import base64
import re
import flask

import dao.users
import dao.utils
import utils.check

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
    cur.execute('delete from usertop', ())
    cur.execute(
        "insert into usertop select userid, cat, cnt, cost from "
        + "(select userid, cat, cnt, cost, "
        + "@rn := if(@cat = cat, @rn+1, if(@cat := cat, 1, 1)) as rn "
        + "from userstats cross join (SELECT @rn := 0, @cat := '') as vars "
        + "order by cat, cnt desc) as t where t.rn <= 10", ())
    cn.commit()
    cur.close()
    return 'ok'


@tools_ctl.route('/wiki/<pageid>')
def wiki_view(pageid):
    if re.match(r'[a-z][a-z0-9\-]*$', pageid) is None:
        flask.abort(404)
    text = dao.utils.query_markdown_blob('wk.' + pageid + '.en')
    if text == '':
        flask.abort(404)
    m = re.search(r'h1\>(.+)\<\/h1', text)
    title = m.group(1) if m is not None else 'Wiki'
    return flask.render_template(
        'wiki.html', title=title, body=text, robots='index,follow')


@tools_ctl.route('/tools/run-code', methods=['POST'])
def run_code():
    data = flask.request.json
    return utils.check.run_code(
        base64.b64decode(data['code']).decode('utf-8'),
        base64.b64decode(data['input']).decode('utf-8'),
        data['lang']
    )


@tools_ctl.route('/.well-known/acme-challenge/<pageid>')
def acme_challenge(pageid):
    path = flask.current_app.root_path
    with open(path + '/../acme-challenge.json') as acme_json:
        data = json.load(acme_json)
        return data.get(pageid, '...no_entry...')
