import flask
import base64
import time
import re

import dao.tasks
import dao.users
import utils.check

tasks_ctl = flask.Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_ctl.route('/')
def task_list():
    info = dao.tasks.list_categories()
    return flask.render_template(
        'tasks/list_cats.html', data=info, robots='index,follow')


@tasks_ctl.route('/view/<id>')
def task_view(id):
    id_clean = "".join([c.lower() for c in id if (c.isalnum() or c == '-')])
    if '-' not in id_clean:
        return task_category(id_clean)
    task_data = dao.tasks.load_one(id_clean)
    if task_data is None:
        flask.abort(404)
    (title, text) = task_data
    if 'username' in flask.session:
        test = load_test_stuff(id_clean, flask.session['userid'])
    else:
        test = None
    data = {'title': title, 'text': text, 'id': id}
    return flask.render_template(
        'tasks/view.html', data=data, test=test, robots='index,follow')


def load_test_stuff(taskid, userid):
    checker_code = dao.tasks.load_checker(taskid)
    if checker_code is None:
        return None
    checker_data = utils.check.checker_exec(checker_code)
    srvsess = dao.users.fetch_srvsession(userid)
    srvsess['expected'] = checker_data['answer']
    srvsess['timeout'] = checker_data['timeout']
    srvsess['curtask'] = taskid
    dao.users.update_srvsession(userid, srvsess)
    return checker_data['input']


def task_category(id):
    cat = dao.tasks.load_category(id)
    if cat is None:
        flask.abort(404)
    info = dao.tasks.load_list(id)
    return flask.render_template(
        'tasks/list.html', cat=cat, data=info, robots='index,follow')


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
    timeout = srvsess['timeout']
    del srvsess['expected'], srvsess['curtask'], srvsess['timeout']
    dao.users.update_srvsession(userid, srvsess)
    answer = utils.check.answer_from_form(expected[0], flask.request.form)
    if answer is None:
        return 'Wooow!'
    solution = flask.request.form.get('solution', None)
    result = process_submission(taskid, expected, timeout, answer, solution)
    return flask.render_template('tasks/check.html', result=result)


def process_submission(taskid, expected, timeout, answer, solution):
    task_type = expected[0]
    expected = expected[1]
    result = {'taskid': taskid, 'catid': re.sub(r'^([a-z]+).*', r'\1', taskid)}
    result['type'] = task_type
    solved = (expected == answer)
    if int(time.time()) > timeout[0]:
        solved = False
        result['timeout'] = timeout[1]
    else:
        result['timeout'] = None
    result['status'] = solved
    if solved:
        result['expl'] = dao.utils.query_markdown_blob('t.' + taskid + '.x.en')
    if task_type == 'plain':
        result['expected'] = expected
        result['answer'] = answer
    elif task_type == 'quiz':
        wrongs = utils.check.quiz_wrong_percentage(expected, answer)
        result['hint'] = str(int(wrongs + 0.5))
    userid = flask.session['userid']
    dao.users.action_log_write(
        userid, 'ATT', taskid + ' ' + ('ok' if solved else 'fail'))
    dao.tasks.update_usertask_record(userid, taskid, solved)
    if solution is not None:
        sol64 = base64.b64encode(solution.encode('utf-8'))
        dao.users.update_userblob(
            'sol.%s.%s.other' % (taskid, userid), sol64)
    return result


@tasks_ctl.route('/sol/<taskid>/<lang>')
def get_solution(taskid, lang):
    userid = flask.session.get('userid')
    if userid is None:
        return 'Too bad request', 400
    key = 'sol.%s.%s.%s' % (taskid, userid, lang)
    res = dao.utils.query_one('userblobs', 'id=%s', (key,), 'val')
    sol = '' if res is None else res[0]
    return (sol, {'Content-Type': 'text/plain'})
