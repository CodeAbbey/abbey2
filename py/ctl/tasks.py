import flask

tasks_ctl = flask.Blueprint('tasks', __name__, url_prefix='/tasks')

task_info = [['prg-1', 'Sample task 1'], ['prg-2', 'Sample task 2'], ['prg-3', 'Sample task 3']]

@tasks_ctl.route('/')
def task_list():
    return flask.render_template('tasks/list.html', data = task_info)

@tasks_ctl.route('/<id>')
def task_view(id):
    found = None
    for item in task_info:
        if item[0] == id:
            found = item
            break
    return flask.render_template('tasks/view.html', data = found)

