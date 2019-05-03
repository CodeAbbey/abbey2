from flask import g, current_app as app
import mysql.connector as mysql

import utils.web


def db_conn():
    if 'db' not in g:
        g.db = mysql.connect(
            user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'], database=app.config['DB_NAME'])
    return g.db


def db_close():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query_list(table, fields='*'):
    cur = db_conn().cursor(buffered=True)
    try:
        cur.execute('select ' + fields + ' from ' + table)
        res = cur.fetchall()
        return res
    except mysql.Error as err:
        return []
    finally:
        cur.close()


def query(table, clause, fields, grplim):
    where = '' if clause is None else (' where ' + clause)
    tail = '' if grplim is None else (' ' + grplim)
    return 'select ' + fields + ' from ' + table + where + tail


def query_one(table, clause, params, fields='*', grplim=None):
    cur = db_conn().cursor(buffered=True)
    cur.execute(query(table, clause, fields, grplim), params)
    res = cur.fetchone()
    cur.close()
    return res


def query_many(table, clause, params, fields='*', grplim=None):
    cur = db_conn().cursor(buffered=True)
    cur.execute(query(table, clause, fields, grplim), params)
    res = cur.fetchall()
    cur.close()
    return res


def query_markdown_blob(bid):
    val = query_one('blobs', "id=%s", (bid,), 'val')
    if val is None:
        return ''
    return utils.web.markdown(val[0].decode('utf-8'))


def execute_change(query, params):
    cn = db_conn()
    cur = cn.cursor()
    cur.execute(query, params)
    cn.commit()
    cur.close()


def update_blob(id, body, blobtable):
    query = 'insert into ' + blobtable + ' (id, val) values (%s, %s)' \
        + ' on duplicate key update val=%s'
    execute_change(query, (id, body, body))
