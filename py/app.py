import flask
from ctl.tasks import tasks_ctl

app = flask.Flask(__name__, static_url_path = '/s')
app.register_blueprint(tasks_ctl)

@app.errorhandler(404)
def page_not_found(e):
  return flask.render_template('404.html'), 404

@app.route('/')
def main_page():
    return flask.render_template('index.html')

@app.route('/login')
def login_page():
    return flask.render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

