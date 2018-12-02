import time
import re

import dao.utils
from utils.time import ts_to_str
from utils.web import markdown


def list_categories():
    res = dao.utils.query_many(
        '(select id, title from tasks where id like \'!%\') c join '
        + '(select concat(\'!\', cat) as id, count(1) as cnt, '
        + 'sum(solved) as slv '
        + 'from taskstats group by cat) s using(id) '
        + 'left join blobs b on concat(\'t.\', c.id, \'.en\')=b.id',
        None, (), 'c.id, title, cnt, slv - cnt, ifnull(b.val, b\'\')')
    return {
        id[1:]: (title, cnt, slv, re.sub(r'\n.*', '', dsc.decode('utf-8')))
        for (id, title, cnt, slv, dsc) in res}


def load_category(cat_id):
    cat_id = '!' + cat_id
    res = dao.utils.query_one(
        'tasks t left join blobs b on concat(\'t.\', t.id, \'.en\')=b.id',
        't.id=%s', (cat_id,), 'title, ifnull(val, b\'\')')
    return None if res is None else res[0], markdown(res[1].decode('utf-8'))


def load_list(cat_id):
    res = dao.utils.query_many(
        'tasks t join taskstats s on id=taskid',
        'id like %s', (cat_id + '-%',), 'id, title, solved-1, cost')
    return {tup[0]: tup[1:] for tup in res}


def load_one(id):
    res = dao.utils.query_one('tasks', 'id=%s', (id,), 'title')
    if res is None:
        return None
    (title,) = res
    text = dao.utils.query_markdown_blob('t.' + id + '.en')
    return (title, text)


def load_checker(id):
    res = dao.utils.query_one(
        'blobs', "id=concat('t.', %s, '.chk')", (id,), 'val')
    return res[0] if res is not None else None


def what_user_tried(userid):
    res = dao.utils.query_many(
        'usertask join tasks on taskid=id', 'userid=%s', (userid,),
        'taskid,solved,title,ts')
    return [(tid, sol, title, ts_to_str(ts)) for (tid, sol, title, ts) in res]


def update_usertask_record(userid, taskid, result):
    res_exists = dao.utils.query_one(
        'usertask', 'userid=%s and taskid=%s', (userid, taskid), 'solved')
    res01 = 1 if result else 0
    cn = dao.utils.db_conn()
    cur = cn.cursor()
    ts = int(time.time())
    if res_exists is None:
        cur.execute(
            'insert into usertask (userid, taskid, solved, ts)'
            + 'values (%s, %s, %s, %s)',
            (userid, taskid, res01, ts))
    elif res_exists[0] < 1:
        cur.execute(
            'update usertask set solved=%s, ts=%s '
            + 'where userid=%s and taskid=%s',
            (result, ts, userid, taskid))
    else:
        return None
    cur.close()
    cn.commit()
