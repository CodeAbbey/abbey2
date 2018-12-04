import os
import json
import time
import flask
from ctl.tasks import tasks_ctl
from ctl.users import users_ctl
from ctl.tools import tools_ctl
import dao.utils
import dao.users
import utils.web
import utils.time


app = flask.Flask(__name__, static_url_path='/s')
app.register_blueprint(tasks_ctl)
app.register_blueprint(users_ctl)
app.register_blueprint(tools_ctl)


@app.route('/')
def main_page():
    def logrec(t):
        if t[2] == 'LOG':
            act = ('entered' if t[3] == '' else 'registered')
        elif t[2] == 'ATT':
            r = t[3].split(' ')
            act = ('solved' if r[1] == 'ok' else 'failed') + ' ' + r[0]
        return (t[1], act, utils.time.ts_ago(t[0]))
    log = dao.users.action_log_recent(20)
    log = [logrec(t) for t in log]
    tasks = dao.utils.query_many('tasks t', "id not like '!%'", (), 'id,title')
    tasks.reverse()
    return flask.render_template(
        'index.html', robots='index,follow', actlog=log, latest=tasks[:13])


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


@app.after_request
def after_all_requests(resp):
    return utils.web.no_cache(resp)


@app.context_processor
def inject_globals():
    return dict(
        stat_ts=int(time.time()/(15*60)),
        canon=utils.web.canonical(),
        robots='noindex,nofollow',
        sitename='OpenAbbey')


@app.teardown_appcontext
def teardown(error):
    dao.utils.db_close()


def config():
    path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_from_file(path + '/config.json')
    additional_cfg = path + '/../.config-custom.json'
    if os.path.isfile(additional_cfg):
        config_from_file(additional_cfg)


def config_from_file(filename):
    with open(filename) as cfg_json:
        cfg = json.load(cfg_json)
        for key in cfg:
            val = cfg[key]
            if isinstance(val, str) and val[0] == '$':
                app.config[key] = os.environ.get(val[1:])
            else:
                app.config[key] = val


config()
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'dummy-key'
    app.run(host='0.0.0.0', port=5000, debug=True)
