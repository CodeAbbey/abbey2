import flask
import mistune

import dao.tasks
import utils.check

tasks_ctl = flask.Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_ctl.route('/')
def task_list():
    info = dao.tasks.list_categories()
    return flask.render_template('tasks/list_cats.html', data=info)


@tasks_ctl.route('/view/<id>')
def task_view(id):
    id_clean = "".join([c.lower() for c in id if (c.isalnum() or c == '-')])
    if '-' not in id_clean:
        return task_category(id_clean)
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
    data = {'title': title, 'text': markdown(text)}
    return flask.render_template('tasks/view.html', data=data, test=test)


def load_test_stuff(taskid, userid):
    checker_code = dao.tasks.load_checker(taskid)
    if checker_code is None:
        return None
    checker_data = utils.check.checker_exec(checker_code)
    srvsess = dao.users.fetch_srvsession(userid)
    srvsess['expected'] = checker_data['answer']
    srvsess['curtask'] = taskid
    dao.users.update_srvsession(userid, srvsess)
    return checker_data['input']


def task_category(id):
    cat_name = dao.tasks.load_category(id)
    if cat_name is None:
        flask.abort(404)
    info = dao.tasks.load_list(id)
    return flask.render_template('tasks/list.html', cat=cat_name, data=info)


@tasks_ctl.route('/check', methods=['POST'])
def task_check():
    if 'username' not in flask.session:
        return 'Oooops!'
    userid = flask.session['userid']
    srvsess = dao.users.fetch_srvsession(userid)
    if ('expected' not in srvsess) or ('curtask' not in srvsess):
        return 'Perhaps, cheating attempt? :)'
    taskid = srvsess['curtask']
    expected = srvsess['expected']
    del srvsess['expected'], srvsess['curtask']
    dao.users.update_srvsession(userid, srvsess)
    answer = utils.check.answer_from_form(expected[0], flask.request.form)
    if answer is None:
        return 'Wooow!'
    result = process_submission(taskid, expected, answer)
    return flask.render_template('tasks/check.html', result=result)


def process_submission(taskid, expected, answer):
    task_type = expected[0]
    expected = expected[1]
    result = {}
    result['type'] = task_type
    result['status'] = (expected == answer)
    if task_type == 'plain':
        result['expected'] = expected
        result['answer'] = answer
    elif task_type == 'quiz':
        wrongs = utils.check.quiz_wrong_percentage(expected, answer)
        result['hint'] = str(int(wrongs + 0.5))
    dao.tasks.update_usertask_record(
        flask.session['userid'], taskid, result['status'])
    return result
