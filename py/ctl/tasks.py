import flask
import mistune

import dao.tasks

tasks_ctl = flask.Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_ctl.route('/')
def task_list():
    info = dao.tasks.list_all()
    return flask.render_template('tasks/list.html', data=info)


@tasks_ctl.route('/view/<id>')
def task_view(id):
    id_clean = "".join([c.lower() for c in id if (c.isalnum() or c == '-')])
    task_data = dao.tasks.load_one(id_clean)
    if task_data is None:
        flask.abort(404)
    (title, text) = task_data
    renderer = mistune.Renderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer)
    if 'username' in flask.session:
        test = load_test_stuff(id_clean, flask.session['userid'])
    else:
        test = None
    data = {'title': title, 'text': markdown(text), 'test': test}
    return flask.render_template('tasks/view.html', data=data)


def load_test_stuff(taskid, userid):
    checker_code = dao.tasks.load_checker(taskid)
    if checker_code is None:
        return None
    local_vars = {}
    exec(checker_code, {}, local_vars)
    srvsess = dao.users.fetch_srvsession(userid)
    srvsess['expected'] = local_vars['expected_answer']
    srvsess['curtask'] = taskid
    dao.users.update_srvsession(userid, srvsess)
    return local_vars['input_data']


@tasks_ctl.route('/check', methods=['POST'])
def task_check():
    form = flask.request.form
    if ('answer' not in form) or ('username' not in flask.session):
        return 'Oooops!'
    userid = flask.session['userid']
    srvsess = dao.users.fetch_srvsession(userid)
    if ('expected' not in srvsess) or ('curtask' not in srvsess):
        return 'Perhaps, cheating attempt? :)'
    taskid = srvsess['curtask']
    result = {}
    result['expected'] = srvsess['expected']
    result['answer'] = flask.request.form['answer']
    result['status'] = (result['expected'] == result['answer'])
    del srvsess['expected'], srvsess['curtask']
    dao.users.update_srvsession(userid, srvsess)
    dao.tasks.update_usertask_record(
        flask.session['userid'], taskid, result['status'])
    return flask.render_template('tasks/check.html', result=result)
