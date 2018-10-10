import dao.utils


def list_all():
    res = dao.utils.query_list('tasks')
    return {id: title for (id, title) in res}


def load_one(id):
    res = dao.utils.query_one('tasks', 'id=%s', (id,), 'title')
    if res is None:
        return None
    (title,) = res
    (text,) = dao.utils.query_one(
        'blobs', "id=concat('t.', %s, '.en')", (id,), 'val')
    return (title, text.decode('utf-8'))


def load_checker(id):
    res = dao.utils.query_one(
        'blobs', "id=concat('t.', %s, '.chk')", (id,), 'val')
    return res[0] if res is not None else None


def what_user_tried(username):
    return dao.utils.query_many(
        'usertask', 'username=%s', (username,), 'taskid,solved,ts')


def update_usertask_record(userid, taskid, result):
    res_exists = dao.utils.query_one(
        'usertask', 'username=%s and taskid=%s', (userid, taskid), 'solved')
    res01 = 1 if result else 0
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    if res_exists is None:
        cur.execute(
            'insert into usertask (username, taskid, solved)'
            + 'values (%s, %s, %s)',
            (userid, taskid, res01))
    elif res_exists[0] < 1:
        cur.execute(
            'update usertask set solved=%s where username=%s and taskid=%s',
            (result, userid, taskid))
    else:
        return None
    cur.close()
    cn.commit()
