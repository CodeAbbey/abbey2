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
        return
    (title, text) = task_data
    renderer = mistune.Renderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer)
    test = load_test_stuff(id_clean)
    data = {'title': title, 'text': markdown(text), 'test': test}
    return flask.render_template('tasks/view.html', data=data)


def load_test_stuff(id):
    checker_code = dao.tasks.load_checker(id)
    if checker_code is None:
        return None
    local_vars = {}
    exec(checker_code, {}, local_vars)
    flask.session['expected-answer'] = local_vars['expected_answer']
    return local_vars['input_data']


@tasks_ctl.route('/check', methods=['POST'])
def task_check():
    form = flask.request.form
    if ('answer' not in form) or ('username' not in flask.session):
        return 'Oooops!'
    result = {}
    result['expected'] = flask.session['expected-answer']
    result['answer'] = flask.request.form['answer']
    result['status'] = (result['expected'] == result['answer'])
    return flask.render_template('tasks/check.html', result=result)
