import dao.utils


def list_categories():
    res = dao.utils.query_many('tasks', "id like '!%%'", (), '*')
    return {id[1:]: title for (id, title) in res}


def load_category(cat_id):
    cat_id = '!' + cat_id
    res = dao.utils.query_one('tasks', 'id=%s', (cat_id,), 'title')
    return None if res is None else res[0]


def load_list(cat_id):
    res = dao.utils.query_many('tasks', "id like %s", (cat_id + '-%',), '*')
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


def what_user_tried(userid):
    return dao.utils.query_many(
        'usertask join tasks on taskid=id', 'userid=%s', (userid,),
        'taskid,solved,title,ts')


def update_usertask_record(userid, taskid, result):
    res_exists = dao.utils.query_one(
        'usertask', 'userid=%s and taskid=%s', (userid, taskid), 'solved')
    res01 = 1 if result else 0
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    if res_exists is None:
        cur.execute(
            'insert into usertask (userid, taskid, solved)'
            + 'values (%s, %s, %s)',
            (userid, taskid, res01))
    elif res_exists[0] < 1:
        cur.execute(
            'update usertask set solved=%s where userid=%s and taskid=%s',
            (result, userid, taskid))
    else:
        return None
    cur.close()
    cn.commit()
