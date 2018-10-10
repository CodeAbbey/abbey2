import dao.utils


def find_with_creds(user, pwd=None):
    if pwd is not None:
        where = 'username=%s and passwd=%s'
        params = (user, pwd)
    else:
        where = 'username=%s'
        params = (user,)
    res = dao.utils.query_one('users', where, params, 'username')
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
