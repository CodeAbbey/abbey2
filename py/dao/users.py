import json
import time

import dao.utils


def find_with_creds(user, pwd=None):
    if pwd is not None:
        where = 'username=%s and passwd=%s'
        params = (user, pwd)
    else:
        where = 'username=%s'
        params = (user,)
    res = dao.utils.query_one('users', where, params, 'id')
    if res is None:
        return None
    (uid,) = res
    return uid


def insert(user, password, email):
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    cur.execute(
        'insert into users (username, passwd, email) values (%s, %s, %s)',
        (user, password, email))
    cn.commit()
    cur.close()


def update_srvsession(userid, value):
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    value = json.dumps(value)
    cur.execute(
        'insert into srvsession (userid, val) values (%s, %s)'
        + ' on duplicate key update val=%s',
        (userid, value, value))
    cn.commit()
    cur.close()


def fetch_srvsession(userid):
    res = dao.utils.query_one('srvsession', 'userid=%s', (userid,), 'val')
    return {} if res is None else json.loads(res[0])


def action_log_write(userid, action, txt):
    timestamp = int(time.time())
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    cur.execute(
        'insert into actionlog (ts,userid,action,txt) values (%s,%s,%s,%s)',
        (timestamp, userid, action, txt))
    cn.commit()
    cur.close()


def action_log_recent(limit):
    return dao.utils.query_many(
        'actionlog join users on userid=id',
        None,
	    (limit,),
        'max(ts) as mts, username, action, txt',
        'group by userid, action, txt order by mts desc limit %s')


def update_userblob(id, body):
    dao.utils.update_blob(id, body, 'userblobs')
