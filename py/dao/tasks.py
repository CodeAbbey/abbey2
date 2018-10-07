import dao.utils


def list_all():
    res = dao.utils.query_list('tasks')
    return {id: title for (id, title) in res}


def load_one(id):
    res = dao.utils.query_one('tasks', "id='" + id + "'", 'title')
    if res is None:
        return None
    (title,) = res
    (text,) = dao.utils.query_one('blobs', "id='t." + id + ".en'", 'val')
    return (title, text.decode('utf-8'))
