from flask import g, current_app as app
import mysql.connector as mysql


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
        print("query_list error: {}".format(err))
        return []
    finally:
        cur.close()


def query_one(table, clause, params, fields='*'):
    cur = db_conn().cursor(buffered=True)
    cur.execute(
        'select ' + fields + ' from ' + table + ' where ' + clause, params)
    res = cur.fetchone()
    cur.close()
    return res


def query_many(table, clause, params, fields='*'):
    cur = db_conn().cursor(buffered=True)
    cur.execute(
        'select ' + fields + ' from ' + table + ' where ' + clause, params)
    res = cur.fetchall()
    cur.close()
    return res
