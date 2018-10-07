import dao.utils


def find_with_creds(user, pwd=None):
    where = "username='" + user
    if pwd is not None:
        where += "' and passwd='" + pwd + "'"
    else:
        where += "'"
    res = dao.utils.query_one('users', where, 'id')
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
