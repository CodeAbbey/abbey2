import flask
import mistune

import dao.tasks

tasks_ctl = flask.Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_ctl.route('/')
def task_list():
    info = dao.tasks.list_all()
    return flask.render_template('tasks/list.html', data=info)


@tasks_ctl.route('/<id>')
def task_view(id):
    id_clean = "".join([c.lower() for c in id if (c.isalnum() or c == '-')])
    task_data = dao.tasks.load_one(id_clean)
    if task_data is None:
        flask.abort(404)
        return
    (title, text) = task_data
    data = {'title': title, 'text': mistune.markdown(text)}
    return flask.render_template('tasks/view.html', data=data)
